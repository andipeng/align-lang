import os
import gym
import cv2
import numpy as np
from einops import rearrange
import enlight.utils as U
import torch
from torchvision.io import write_video


class VisualizationWrapper(gym.Wrapper):
    def __init__(self, env, *, save_path: str):
        assert env.get_multi_modal_prompt_img is not None
        super().__init__(env)

        self._save_path = save_path
        os.makedirs(self._save_path, exist_ok=True)

        self._rgbs = []
        self._final_rgbs = []
        self._actions = []
        self._prompt_img = None

        self._pos_bound_low = env.position_bounds.low[:2]
        self._pos_bound_high = env.position_bounds.high[:2]

        self._n_saved = 0

    def reset(self):
        self._rgbs = []
        self._final_rgbs = []
        self._actions = []

        rtn = self.env.reset()
        self._prompt_img = self.env.get_multi_modal_prompt_img()
        self._rgbs.append(rtn["rgb"]["top"])
        return rtn

    def step(self, action, **kwargs):
        self._actions.append(
            {
                "pos0": action["pose0_position"][:2],
                "pos1": action["pose1_position"][:2],
            }
        )
        obs, reward, done, info = self.env.step(action, **kwargs)
        if done:
            self._final_rgbs.append(obs["rgb"]["top"])
            self._final_rgbs.append(obs["rgb"]["front"])
            successful, failed = info["success"], info["failure"]
            timeout = not successful and not failed
            self._save_video(successful, failed, timeout)
        else:
            self._rgbs.append(obs["rgb"]["top"])
        return obs, reward, done, info

    def _save_video(self, success, failed, timeout):
        assert len(self._rgbs) == len(self._actions)
        annotated_rgbs = []
        for rgb, action in zip(self._rgbs, self._actions):
            _, h, w = rgb.shape
            pos0, pos1 = action["pos0"], action["pos1"]
            # normalize to [0, 1] then scale to image size
            pos0 = (pos0 - self._pos_bound_low) / (
                self._pos_bound_high - self._pos_bound_low
            )
            pos1 = (pos1 - self._pos_bound_low) / (
                self._pos_bound_high - self._pos_bound_low
            )
            pos0 = pos0 * np.array([h, w])
            pos1 = pos1 * np.array([h, w])
            # annotate rgb
            rgb = rearrange(rgb.copy(), "c h w -> h w c")
            # RGB -> BGR
            rgb = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
            # draw circles
            rgb = cv2.circle(rgb, tuple(pos0.astype(np.int32)[::-1]), 5, (0, 0, 255), 2)
            rgb = cv2.circle(rgb, tuple(pos1.astype(np.int32)[::-1]), 5, (0, 255, 0), 2)
            # put text
            rgb = cv2.putText(
                rgb,
                " pick",
                org=tuple(pos0.astype(np.int32)[::-1]),
                fontScale=0.5,
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                color=(0, 0, 255),
                thickness=1,
                lineType=cv2.LINE_AA,
            )
            rgb = cv2.putText(
                rgb,
                " place",
                org=tuple(pos1.astype(np.int32)[::-1]),
                fontScale=0.5,
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                color=(0, 255, 0),
                thickness=1,
                lineType=cv2.LINE_AA,
            )
            # BGR -> RGB
            rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
            annotated_rgbs.append(rgb)
        # pad prompt image (H, W, 3) to the same ratio as the annotated rgbs
        prompt_img = self._prompt_img.copy()
        h_p, w_p, _ = prompt_img.shape
        target_ratio = h / w
        if h_p / w_p < target_ratio:
            # pad height
            diff = int(w_p * target_ratio) - h_p
            pad_top = diff // 2
            pad_bottom = diff - pad_top
            prompt_img = np.pad(
                prompt_img,
                pad_width=((pad_top, pad_bottom), (0, 0), (0, 0)),
                mode="constant",
                constant_values=0,
            )
        else:
            # pad width
            diff = int(h_p / target_ratio) - w_p
            pad_left = diff // 2
            pad_right = diff - pad_left
            prompt_img = np.pad(
                prompt_img,
                pad_width=((0, 0), (pad_left, pad_right), (0, 0)),
                mode="constant",
                constant_values=0,
            )
        # make h and w of prompt image to be even
        h_p, w_p, _ = prompt_img.shape
        h_p = h_p + (h_p % 2)
        w_p = w_p + (w_p % 2)
        prompt_img = cv2.resize(prompt_img, (w_p, h_p))
        # resize annotated rgbs to the same size as the prompt img
        target_h, target_w, _ = prompt_img.shape
        annotated_rgbs = [
            cv2.resize(rgb, (target_w, target_h), interpolation=cv2.INTER_AREA)
            for rgb in annotated_rgbs
        ]
        resized_final_rgbs = []
        for rgb in self._final_rgbs:
            rgb = rearrange(rgb.copy(), "c h w -> h w c")
            rgb = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
            rgb = cv2.resize(rgb, (target_w, target_h), interpolation=cv2.INTER_AREA)
            rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
            resized_final_rgbs.append(rgb)
        annotated_rgbs = annotated_rgbs + resized_final_rgbs

        # concatenate prompt image and annotated rgbs along height
        final_rgbs = []
        for rgb in annotated_rgbs:
            final_rgbs.append(np.concatenate([rgb, prompt_img], axis=0))
        final_rgbs = np.stack(final_rgbs, axis=0)
        # save video
        video = U.any_to_torch_tensor(final_rgbs, dtype=torch.uint8)
        write_video(
            U.f_join(
                self._save_path,
                f"video_{self._n_saved}_succ{success}_fail{failed}_timeout{timeout}.mp4",
            ),
            video,
            fps=1,
        )
        self._n_saved += 1
