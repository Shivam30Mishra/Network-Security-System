'''
The setup.py file is an essential part of packaging and distributing python projects. It is used by setup tools(or distutils in older Python Versions) to define the configuration of your project such as it's metadata, dependencies and more
'''

from setuptools import find_packages, setup
from typing     import List

def get_requirements()->List[str]:
  """
  This function will return list of requirements
  """
  requirement_lst:List[str]=[]
  try:
    with open('requirements.txt','r') as file:
      # Read lines from the files
      lines = file.readlines()
      # process each lines
      for line in lines:
        requirement = line.strip()
        # ignore empty line and -e
        if requirement and requirement!='-e .':
          requirement_lst.append(requirement)
  except FileNotFoundError:
    print("requirements.txt file not found")
  return requirement_lst

print(get_requirements())

setup(
  name="NetworkSecurity",
  version="0.0.1",
  author="Shivam Mishra",
  author_email="theshivammishra10@gmail.com",
  packages=find_packages(),
  install_requires=get_requirements()
)