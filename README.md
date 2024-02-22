# AI beats

![](./assets/ai_trailer.jpg)

---

The idea of this repository is to automatically generate a number of trailer candidates for a given movie, the user only needs to provide the movie file and a couple of text parameters, and everything else is taken care.

### How does it works?
First, we take the movie's plot at IMDB and split it into subplots, they will roughly describe the main parts of the movie, and next, we generate a voice for each subplot. Now that we have the spoken part of the trailer we just need to take short clips corresponding to each subplot and apply the voice over them, we do this by sampling many frames from the movie and taking some of the most similar frames to each subplot, with this we have the images that best represent each subplot, the next step would be to take a clip of a few seconds starting from each frame. After generating the audio and visual part of the trailer we just need to combine each audio with the corresponding clip and finally join all clips together into the final trailer.

All of those steps will generate intermediate files that you can inspect and manually remove what you don't like to improve the results.

> Note: with the default parameters, for each subplot only one audio and one clip will be generated thus creating only one trailer candidate. If you wish to create more trailer candidates or have more options of audios and clips to choose from, you can increase `n_audios` and `n_retrieved_images`, just keep in mind that the trailer candidates increase geometrically with this, for `n_audios = 3` and `n_retrieved_images = 3` you will have 9 (3**3) trailer candidates at the end.

# Examples
### Night of the Living Dead (1968)
[![Watch the video](https://i.ytimg.com/vi/qNt4fQlEHPA/hqdefault.jpg)](https://youtu.be/qNt4fQlEHPA)

### Nosferatu (1922)
[![Watch the video](https://i.ytimg.com/vi/bfUdjzndOyI/hqdefault.jpg)](https://youtu.be/bfUdjzndOyI)

# Usage
The recommended approach to use this repository is with [Docker](https://docs.docker.com/), but you can also use a custom venv, just make sure to install all dependencies.

**The user only needs to provide two inputs**, the movie file and the IMDB ID from that movie.
After that you can go to the `configs.yaml` file and adjust the values accordingly, `movie_id` will be the IMDB ID, and `movie_path` should point to the movie's file, you might also want to update `project_name` to your movie's name and provide a reference voice with `reference_voice_path`.

## Application workflow
1. **Plot:** Get the movie's plot from IMDB and split it into subplots
2. **Voice:** Generate a voice for each subplot

## Configs
```
project_name: night_of_the_living_dead
```
- **project_name**: Project name and main folder, it can be any name that you want

## Commands
Build the Docker image
```bash
make build
```

Apply lint and formatting to the code (only needed for development)
```bash
make lint
```

# Development
For development make sure to install `requirements-dev.txt` and run `make lint` to maintain the the coding style.

# Disclaimers
By default I am using [XTTS](https://huggingface.co/coqui/XTTS-v2) from [Coqui AI](https://github.com/coqui-ai/TTS) the model is under the [Coqui Public Model License](https://coqui.ai/cpml) make sure to take a look there if you plan to use the outputs here.