import { useActiveSpeakerId, useMediaTrack, useParticipant } from '@daily-co/daily-react';
import { useEffect, useRef } from 'react';

const Tile = ({id, isScreenShare}: {
  id: string,
  isScreenShare: boolean
}) => {
  const participant = useParticipant(id);
  const activeSpeakerId = useActiveSpeakerId();
  const videoTrack = useMediaTrack(id, isScreenShare ? 'screenVideo' : 'video');
  const audioTrack = useMediaTrack(id, isScreenShare ? 'screenAudio' : 'audio');
  const videoElement = useRef<HTMLVideoElement>(null);
  const audioElement = useRef<HTMLAudioElement>(null);

  function render() {
    return(
      <div className={
        `${isScreenShare ? 'tile-screenshare' : 'tile-video'} 
        w-[240px] h-[135px] relative
        `}
      >
        {participant?.user_name && 
          <span className="absolute bottom-1 left-2 text-white bg-gray-800 text-sm px-2 py-1.5 bg-opacity-90 text-xs">
            {participant?.user_name}
          </span>
        }
        {videoTrack && <video autoPlay muted playsInline ref={videoElement} 
          className={`rounded-lg ${activeSpeakerId === id ? 'border-4 border-yellow-600 border-solid' : 'border-4 border-transparent'}`} />}
        {audioTrack && <audio autoPlay playsInline ref={audioElement} />}
      </div>
    )
  }

  useEffect(() => {
    /*  The track is ready to be played. We can show video of the remote participant in the UI.*/
    if (videoTrack?.state === 'playable') {
      videoElement.current &&
        (videoElement.current.srcObject =
          videoTrack && new MediaStream([videoTrack.persistentTrack]));
    }
  }, [videoTrack]);

  useEffect(() => {
    if (audioTrack?.state === 'playable') {
      audioElement?.current &&
        (audioElement.current.srcObject =
          audioTrack && new MediaStream([audioTrack.persistentTrack]));
    }
  }, [audioTrack]);

  return render()
}

export default Tile