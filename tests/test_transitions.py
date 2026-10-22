import sys
from pathlib import Path
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from preview_transitions import animation_plan,frame_at,rendered_frame,selected_state


class TransitionTests(unittest.TestCase):
    def test_running_natural_exit_starts_slow_idle_at_2460ms(self):
        self.assertEqual((frame_at('running',2459).row,frame_at('running',2459).column),(7,5))
        self.assertEqual((frame_at('running',2460).row,frame_at('running',2460).column),(0,0))
        self.assertEqual(frame_at('running',4139).column,0)
        self.assertEqual(frame_at('running',4140).column,1)

    def test_idle_keeps_unequal_sixfold_frame_durations(self):
        frames,start=animation_plan('idle')
        self.assertEqual([f.ms for f in frames],[1680,660,660,840,840,1920])
        self.assertEqual(sum(f.ms for f in frames),6600)
        self.assertEqual(start,0)
        self.assertEqual(frame_at('idle',6600).column,0)

    def test_explicit_loop_does_not_fall_back_to_idle(self):
        self.assertEqual(frame_at('running',3000,loop=True).row,7)
        self.assertEqual(frame_at('running',3000).row,0)

    def test_drag_overrides_hover_and_hover_overrides_business(self):
        self.assertEqual(selected_state('failed',hover=True),'jumping')
        self.assertEqual(selected_state('failed',hover=True,drag='running-left'),'running-left')
        self.assertEqual(selected_state('failed'),'failed')

    def test_look_is_static_only_for_eligible_visual_states(self):
        self.assertEqual((rendered_frame('running',3000,look=4).row,rendered_frame('running',3000,look=4).column),(9,4))
        self.assertEqual(rendered_frame('running',0,hover=True,look=4).row,4)
        self.assertEqual(rendered_frame('running',0,drag='running-right',look=4).row,1)
        self.assertEqual(rendered_frame('waiting',0,look=4).row,6)

    def test_reduced_motion_stays_on_requested_first_frame(self):
        frame=rendered_frame('running',100000,reduced_motion=True)
        self.assertEqual((frame.row,frame.column),(7,0))
        self.assertEqual(rendered_frame('running',100000,look=8,reduced_motion=True).row,10)

    def test_bad_state_override_and_direction_are_rejected(self):
        with self.assertRaises(ValueError):selected_state('running',drag='waiting')
        with self.assertRaises(ValueError):rendered_frame('idle',0,look=16)


if __name__=='__main__':unittest.main()
