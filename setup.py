from setuptools import setup, find_packages

with open('README.md') as readme_file:
    long_description = readme_file.read()

setup(name='GPSconverter',
      version='0.0.15',
      description='Python package for manipulating gps data and easily convert them to other different formats.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url="https://github.com/carmelosammarco/GPSconverter",
      author='Carmelo Sammarco',
      author_email='sammarcocarmelo@gmail.com',
      license='gpl-3.0',
      zip_safe=False,
      platforms='OS Independent',
      python_requires='~=3.6',

      include_package_data=True,
      package_data={
        'GPSconverter': ['DATA/LOGO.gif']

      },

      install_requires=[
        'gpxpy >= 1.4.0',
        'numpy >= 1.18.1',
        'pandas >= 1.0.3',
        'scipy >= 1.4.1',
        'folium >= 0.12.1',
        'Flask >= 2.0.1',
        'Pillow >= 8.2.0',
        'simplekml >= 1.3.5',
        'tkmacosx >= 1.0.3',
        'html2image >= 1.1.3',
        #'fiona>= 1.8.4',
        #'geopandas >= 0.9.0',
        'pyshp >= 2.1.3',
        'matplotlib >= 3.4.2',
        'pygmt'
        
        
      ],
      
      packages=find_packages(),

      entry_points={
        'console_scripts':['GPSconverter = GPSconverter.__main__:main']
        
      },

      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3.8',
       ], 

)
