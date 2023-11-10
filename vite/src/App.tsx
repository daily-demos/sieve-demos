import { useState } from "react";

const apiURL = 'http://127.0.0.1:5000';


type DailyRecording = {
  id: string;
  room_name: string;
  timestamp: string;
}

type ProcessedVideo = {
  recording_id: string;
  original_video: string;
  processed_video: string;
}

function App() {
  
  function render() {
    return(
    <div className="bg-daily-gray-950 min-h-screen h-full">
      <div className="container mx-auto py-16">
        <h1 className="text-dailyGray50 text-[50px] pb-6 mb-9 border-dailyGray50 border-b">AI Video Processing - Daily + Sieve</h1>

        <div className="grid grid-cols-3 gap-4">
          <aside>
            <button onClick={getRecordings} className="px-4 py-3 bg-dailyOrange text-white rounded">Fetch recordings</button>
            <ul className="mt-6 max-h-screen overflow-y-scroll">
              {recordings?.map(r => (
                <li key={r.id}
                className="mb-3 text-dailyGray50 hover:bg-dailyGray900 py-4 px-6 rounded flex flex-col gap-5">
                  <div>
                    <div className="text-sm">{r.timestamp}</div>
                    <div className="text-xs">{r.id}</div>
                    <div className="text-xs text-dailyGray400">Room: {r.room_name}</div>
                  </div>
                  <div className="flex gap-3">
                    <button onClick={() => processRecording('audio_enhance', r.id)} className={`px-3 py-1.5 bg-dailyDarkSky hover:bg-dailyDarkSkyHover rounded text-white border-solid text-sm`}>Enhance audio</button>
                    <button onClick={() => processRecording('text_to_video_lipsync', r.id)} className={`px-3 py-1.5 bg-dailyDarkOlive hover:bg-dailyDarkOliveHover rounded text-white border-solid text-sm`}>TTS Lipsync</button>
                    <button onClick={() => processRecording('video_dubbing', r.id)} className={`px-3 py-1.5 bg-dailyOrange hover:bg-dailyOrangeHover rounded text-white border-solid text-sm`}>Translate & Dub</button>
                  </div>
                </li>
              ))}
            </ul>
          </aside>
          <ul className="grid grid-cols-2 gap-3 w-full col-span-2">
            {!isProcessing && processedVideo &&
              <>
              <div className="text-center text-gray-500">
                <video controls width="750" height="500" src={`${processedVideo?.original_video}`}/>
                <p className="mt-4">Original video</p>
              </div>
              <div className="text-center text-white">
                <video controls width="750" height="500" src={`/${processedVideo?.processed_video}`}/>
                <p className="mt-4">Processed video</p>
              </div>
              </>
            }
            {isProcessing &&
              <p className="text-white">Processing recording...This may take a few minutes. Check your Python logs to follow along!</p>
            }
          </ul>
        </div>
      </div>
    </div>
    )
  }

  const [recordings, setRecordings] = useState<DailyRecording[]>();
  const [processedVideo, setProcessedVideo] = useState<ProcessedVideo>();
  const [isProcessing, setIsProcessing] = useState<boolean>(false);

  function getRecordings() {
    fetch(`${apiURL}/recordings`, { method: 'GET' })
      .then((res) => {
        if (res.ok === false) {
          throw Error(`Fetching recordings failed: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        const { recordings } = data;
        if (recordings) {
          setRecordings(recordings);
        }
      })
      .catch((e) => {
        console.error('Failed to process video:', e);
      });
  }

  function processRecording(endpoint: string, recording_id: string) {
    setIsProcessing(true);

    fetch(`${apiURL}/${endpoint}/${recording_id}`, { method: 'POST' })
    .then((res) => {
      if (res.ok === false) {
        setIsProcessing(false);
        throw Error(`Process recording request failed: ${res.status}`);
      }
      return res.json();
    })
    .then((data) => {
      setIsProcessing(false);
      console.log('Successfully processed video data:', data)
      setProcessedVideo(data);
    })
    .catch((e) => {
      setIsProcessing(false);
      console.error('Failed to process recording:', e);
    });
  }

  return render();
}



export default App
