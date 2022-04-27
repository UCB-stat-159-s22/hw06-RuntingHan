.PHONY: env
env: 
	mamba env create -f environment.yml -p ~/envs/ligo06
	conda activate ligo
	python -m ipykernel install --user --name ligo --display-name "IPython - ligo-06"
    
    
.PHONY: html
html:
  jupyter-book build .
  
  
.PHONY: html-hub
html-hub:   
	jupyter-book config sphinx .
	sphinx-build  . _build/html -D html_baseurl=${JUPYTERHUB_SERVICE_PREFIX}/proxy/absolute/8000
	@echo "https://stat159.datahub.berkeley.edu/user-redirect/proxy/8000/index.html"
    
    
.PHONY: clean
clean:
	rm -f figurs/*.png
	rm -f audio/*.wav
	rm -rf _build/*
    
  
    
