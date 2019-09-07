from threading import Thread
import numpy as np
from .alg import LinUCB
from .scenario import Scenario
from .stats import Stats

ACTIONS = [0, 1, 2, 3]


class Recommender:
  def __init__(self, evt_dim=4):
    ctx_size = evt_dim + len(ACTIONS)
    self.model = LinUCB(ctx_size, len(ACTIONS))
    self.stats = Stats(len(ACTIONS), expire_after=1800)

    # temp mock revward
    self.mock_scenario = Scenario(evt_dim, len(ACTIONS))


  def dispatch(self, speaker_id, evt):
    if not isinstance(evt, np.ndarray):
      evt = np.array(evt)

    thread = Thread(target=self._process_evt, args=(speaker_id, evt))
    thread.start()


  def _process_evt(self, speaker_id, evt):
    self.stats.refresh_vct()
    ctx = np.concatenate([evt, self.stats.vct])

    action_idx = self.model.act(ctx)

    if action_idx is None:
      print('No action')
      return

    action = ACTIONS[action_idx]
    err = self._send_action(action)

    # if send recommendation successfully
    if not err:
      reward = self.get_reward(ctx, action_idx)
      self.model.update(ctx, action_idx, reward)

  def get_reward(self, ctx, action_idx):
    '''
    temp mocked reward
    '''

    reward, _ = self.mock_scenario.insight(0, ctx, action_idx)

    return reward


  def _send_action(self, action):
    '''
    Send the chosen action to the downstream
    return err if any
    '''

    err = None

    # TODO actutal logic to send the data
    print('Action', action)


    # return err if any
    return err

