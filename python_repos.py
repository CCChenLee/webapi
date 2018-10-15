#!/usr/bin/env python3
#-*- coding:utf-8 -*-

"""
使用Pygal可视化仓库
呈现Github上Python项目的受欢迎程度
创建交互式条形图，高度代表项目获得的星数
点击则进入项目在Github的主页上
"""
import requests

import pygal

from pygal.style import LightColorizedStyle as LCS,LightenStyle as LS

#执行API调用并存储响应
url = "https://api.github.com/search/repositories?q=language:python&sort=stars"
r = requests.get(url)
print("Status code: ",r.status_code)

#将API响应存储在一个变量中
response_dict = r.json()
# 指出github总共多少个python仓库
print("Total repositories: ",response_dict['total_count'])

#探索获得有多少个仓库的信息
repo_dicts = response_dict['items']
# print("Repositories returned: ",len(repo_dicts))
print("Number of items: ",len(repo_dicts))


#研究第一个仓库
# repo_dict = repo_dicts[0]
# print("\nKeys: ",len(repo_dict))
# for key in sorted(repo_dict.keys()):
# 	print(key)

# repo_dict = repo_dicts[0]
#打印了表示第一个仓库的字典中与很多键相关联的值
# print("\nSelected information about first repository:")
# print('Name: ',repo_dict['name'])
# print('Owner: ',repo_dict['owner']['login'])
# print('Stars: ',repo_dict['stargazers_count'])
# print('Repository: ',repo_dict['html_url'])
# print('Created: ',repo_dict['created_at'])
# print('Updated: ',repo_dict['updated_at'])
# print('Description: ',repo_dict['description'])

# 打印API调用返回每个仓库的特定信息，以便能够在可视化中包含这些信息
# print("\nSelected information about each repository:")
# for repo_dict in repo_dicts:
# 	print('\nName: ',repo_dict['name'])
# 	print('Owner: ',repo_dict['owner']['login'])
# 	print('Stars: ',repo_dict['stargazers_count'])
# 	print('Respository: ',repo_dict['html_url'])
# 	print('Description: ',repo_dict['description'])

# print(response_dict.keys())

# names,stars = [],[]
names,plot_dicts = [],[]
for repo_dict in repo_dicts:
	names.append(repo_dict['name'])
	# stars.append(repo_dict['stargazers_count'])
	"""
	若没有if的话会出现如下报错：
	 	File "C:/ProgramData/Anaconda3/lib/site-packages/pygal/util.py", line 233,
	  in decorate metadata['label'])
		File "C:/ProgramData/Anaconda3/lib/site-packages/pygal/_compat.py", line 61, 
		  in to_unicode
		 return string.decode('utf-8')
		AttributeError: 'NoneType' object has no attribute 'decode'
		猜测是因为其中有个参数(repo_dict的description)为none，无属性，
		对此参数加上是否为none的if--else判断，运行通过
	"""
	if repo_dict['description']:
		plot_dict = {
			'value':repo_dict['stargazers_count'],
			'label':repo_dict['description'],
			'xlink':repo_dict['html_url'], #每个条形作为网站的链接
		}
		plot_dicts.append(plot_dict)
	else:
		plot_dict = {
			'value':repo_dict['stargazers_count'],
			'label':'ABCDEFGHIJKLNMOPQRSTUVWXYZ',
			'xlink':repo_dict['html_url'],
		}
		plot_dicts.append(plot_dict)

# 可视化
my_style = LS('#333366',base_style=LCS)
# chart = pygal.Bar(style=my_style,x_label_rotation=45,show_legend=False) #旋转45度，隐藏图例

my_config = pygal.Config() #创建Pygal类Config的实例
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size = 14
my_config.major_label_font_size = 18
my_config.truncate_label = 15 #将较长的项目名缩短为15哥字符，鼠标指向则完整显示出来
my_config.show_y_guides = False #隐藏图表中的水平线
my_config.width = 1000
chart = pygal.Bar(my_config,style=my_style)

chart.title = 'Most-Starred Python Projects on Github'
chart.x_labels = names
# chart.add('',stars)
chart.add('',plot_dicts)
chart.render_to_file('python_repos.svg')