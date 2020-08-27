# time-tracker

Despite what the title might lead you to believe, this doesn't track all my time, but only a very specific subset of my time, i.e. the time I spend at work waiting for an image to go through the build/deploy pipeline. The GitOps tooling at work can be a little buggy and I feel like I spend a lot of my time waiting and retrying failed builds. This is just a quick way to quantify the amount of time I'm actually waiting (versus what I _feel_ like I've waited because who doesn't want instantaneous deployment) because a) I'm genuinely curious and b) I want to be able to have concrete data to bring this up in 1-1s re. the amount of time and company money that's spent trying to execute a basic task using our provided tools.

This isn't anything fancy, just a bash script that exports the necessary environment variables (start time, end time) and then calls a python script using @jamalex's [notion-py](https://github.com/jamalex/notion-py) library to write that info to an already created Notion table because I find Notion more aesthetically pleasing than postgres :) Also I already have it open all day to take notes.

The only env vars you need to supply are the token_v2 and URL of the notion page you want to edit so you can use notion-py (explained in that library's readme).
