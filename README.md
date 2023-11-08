
## Sieve AI Processing of Daily Video Call Recordings

This demo provides three sample use cases for applying cloud-based AI functions from Sieve on Daily video call recordings.

## Running the demo locally

This demo was tested with Python version 3.11.6. We recommend running this in a virtual environment.

### Set up your environment

Ensure that you have [FFmpeg](https://ffmpeg.org/) installed on your machine.

1. Clone this repository.
1. Copy the `.env.sample` file into `.env`. DO NOT submit your `.env` file to version control.
1. Update your `.env` with your `DAILY_API_KEY`

### Create and activate a virtual environment

In the root of the repository on your local machine, run the following commands:

1. `python3 -m venv venv`
1. `source venv/bin/activate`

### Run the application

In the virtual environment, run the following: 

1. Run `pip install -r requirements.txt` from the root directory of this repo on your local machine.
1. **Starting the server:** Run `quart --app server/index.py --debug run` in your terminal.
1. **Starting the client:** Inside the `vite` directory, run `npm install` followed by `npm run dev`

Now, open the localhost address shown in your terminal after the last step above, which should be `localhost:5173`. You should see the front-end of the demo allowing you to fetch your latest Daily recordings.

## How it works

This demo starts by allowing users to fetch their latest Daily video recordings, using the Daily API. Once obtained, users are presented with three choices for running Sieve functions to run on their Daily recordings. This includes the following:

1. `audio_enhancement` - https://www.sievedata.com/functions/sieve/audio_enhancement
1. `text_to_video_lipsync` - https://www.sievedata.com/functions/sieve/text_to_video_lipsync
1. Video Dubbing, which comprises of _four different Sieve functions_:
  1. `speech_transcriber` - https://www.sievedata.com/functions/sieve/speech_transcriber
  1. `seamless_text2text` - https://www.sievedata.com/functions/sieve/seamless_text2text
  1. `xtts-v1` - https://www.sievedata.com/functions/sieve/xtts-v1
  1. `video_retalking` - https://www.sievedata.com/functions/sieve/video_retalking

All Sieve functions follow more or less the same usage, which is as follows:

1. Upload your video or audio to Sieve
1. Fetch the Sieve function of your choice
1. Run the Sieve function

For example:

```
import sieve

# Step 1: Upload your video/audio to Sieve
audio = sieve.Audio(url="https://storage.googleapis.com/sieve-prod-us-central1-public-file-upload-bucket/79543930-5a71-45d9-b690-77f4f0b2bfaa/1a704dda-d8be-4ae1-9894-b4ee63c69567-input-audio.mp3")

# Step 2: Fetch the Sieve function of your choice:
audio_enhancement = sieve.function.get("sieve/audio_enhancement")

# Step 3: Run the Sieve function (and capture the output)
filter_type = "all"
enhance_speed_boost = False
enhancement_steps = 50

output = audio_enhancement.run(audio, filter_type, enhance_speed_boost, enhancement_steps)
```

## Caveats

Closer inspection of this demo code will reveal that not all Daily recordings are passed in to Sieve functions _as is_. 

For example, for both of the lip-syncing demos, we had to shave off the first second of the Daily recording since they begin with a brief black screen instead of the speaker's face. Additionally, the lip-syncing functions tend not to work on videos where there are more than one active speaker. **Input requirements for each Sieve function is clearly outlined in their README files available on Sieve's website**, so be sure to reference those when trouble-shooting.

It's also worth noting that the demos in this app solely rely on standard Daily recording formats, but more possibilities open up when using Sieve functions on **Daily raw track recordings**, so if you're looking for something more custom, that's something to look into!

### Security

This demo contains no authentication features. Processed videos are placed into a public folder that anyone can reach, associated with a UUID. Should a malicious actor  guess or brute-force a valid project UUID, they can download processed output associated with that ID. For a production use case, access to output files should be gated.

### Error handling

This demo implements basic error handling in the form of writing errors to `stderr`. For a production use-case, appropriate logging and metrics should be added.