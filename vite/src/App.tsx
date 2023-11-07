import { SyntheticEvent, useEffect, useRef, useState } from "react";

const apiURL = 'http://127.0.0.1:5000';

type Project = {
  name: string,
  project_id: string,
  status?: ProjectStatus,
  downloadLink?: string,
}

type ProjectStatus = 'Not started' | 'In progress' | 'Succeeded' | 'Failed'
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
            {processedVideo &&
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
            {/* <video controls width="750" height="500" src={`/public/${originalVideo}`}/> */}
            {/* {summaries?.map(s => (
              <li key={s.recording_id} 
              className="text-dailyGray50 bg-dailyGray900 rounded-lg p-6 flex flex-col gap-3">
                <div className="flex justify-between">
                  <span className="text-dailyGray50 text-sm">{s.timestamp}</span>
                  <a href={s.access_link} className="text-dailyOrange text-sm">Watch recording</a>
                </div>
                <h2 className="text-xl">{s.title}</h2>
                <p className="text-sm">{s.summary}</p>
                <ul className="flex gap-2 flex-wrap">
                  {s.tags.map(t => (
                    <li key={t} className="shrink-0 text-xs rounded-lg bg-dailyDarkOlive px-2 py-1">{t}</li>
                  ))}
                </ul>
              </li>
            ))} */}
          </ul>
        </div>
      </div>
    </div>
    )
  }

  const [recordings, setRecordings] = useState<DailyRecording[]>()
  const [processedVideo, setProcessedVideo] = useState<ProcessedVideo>()
  const [hoveredRecording, setHoveredRecording] = useState<string>()

  function getRecordings() {
    fetch(`${apiURL}/recordings`, { method: 'GET' })
      .then((res) => {
        if (res.ok === false) {
          throw Error(`upload request failed: ${res.status}`);
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
        console.error('Failed to process uploaded video:', e);
      });
  }

  function processRecording(endpoint: string, recording_id: string) {
    fetch(`${apiURL}/${endpoint}/${recording_id}`, { method: 'POST' })
    .then((res) => {
      if (res.ok === false) {
        throw Error(`upload request failed: ${res.status}`);
      }
      return res.json();
    })
    .then((data) => {
      console.log(data)
      setProcessedVideo(data);
      // setSummaries([...summaries, data])
    })
    .catch((e) => {
      console.error('Failed to process uploaded video:', e);
    });
  }
  

  return render();
}



export default App
