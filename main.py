from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy
from env import AppleBasket

import os

env = AppleBasket()

def check():
	episodes = 50
	for episode in range(1, episodes+1):
		state = env.reset()
		done = False
		score = 0 
		
		while not done:
			action = env.action_space.sample()
			n_state, reward, done, info = env.step(action)
			score+=reward
			env.render("mode")
		print('Episode:{} Score:{}'.format(episode, score))
	env.close()

def train():
	log_path = os.path.join('Training', 'Logs')
	model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=log_path)
	model.learn(total_timesteps=100000)
	model.save('PPO-100000')

def test():
	log_path = os.path.join('PPO.zip')
	model = PPO.load(log_path, env)
	evaluate_policy(model, env, n_eval_episodes=10, render=True)

train()