import { useAudioTrack, useDaily, useLocalParticipant, useScreenShare, useVideoTrack } from '@daily-co/daily-react';
import React, { useCallback, useState } from 'react';
import { CameraOff, CameraOn, Info, Leave, MicrophoneOff, MicrophoneOn, Screenshare } from './Icons';

const Tray = ({ leaveCall}: {
  leaveCall: () => void
}) => {
  const callObject = useDaily();
  const localParticipant = useLocalParticipant();
  if (!localParticipant) return;
  const { isSharingScreen, startScreenShare, stopScreenShare } =
    useScreenShare();
    const [showMeetingInformation, setShowMeetingInformation] = useState(false);

  const localVideo = useVideoTrack(localParticipant?.session_id);
  const localAudio = useAudioTrack(localParticipant?.session_id);

  const mutedVideo = localVideo.isOff;
  const mutedAudio = localAudio.isOff;

  function render() {
    return(
      <div className="flex justify-between py-4 px-6 text-xs">
        <div className="flex gap-4">
          <button className="w-24 flex flex-col items-center" onClick={toggleVideo}>
            {mutedVideo ? <CameraOff /> : <CameraOn />}
            {mutedVideo ? 'Turn camera on' : 'Turn camera off'}
          </button>
          <button className="w-24 flex flex-col items-center" onClick={toggleAudio}>
            {mutedAudio ? <MicrophoneOff /> : <MicrophoneOn />}
            {mutedAudio ? 'Unmute mic' : 'Mute mic'}
          </button>
        </div>
        <div className="flex gap-4">
          <button className="w-24 flex flex-col items-center" onClick={toggleScreenShare}>
            <Screenshare />
            {isSharingScreen ? 'Stop sharing screen' : 'Share screen'}
          </button>
          <button className="w-24 flex flex-col items-center" onClick={toggleMeetingInformation}>
            <Info />
            {showMeetingInformation ? 'Hide info' : 'Show info'}
          </button>
        </div>
        <div className="flex gap-4">
          <button className="w-24 flex flex-col items-center" onClick={leave}>
            <Leave /> Leave call
          </button>
        </div>
      </div>
    )
  }

  const leave = () => {
    leaveCall();
  };

  const toggleScreenShare = () =>
    isSharingScreen ? stopScreenShare() : startScreenShare();

  const toggleVideo = useCallback(() => {
    callObject!.setLocalVideo(mutedVideo);
   }, [callObject, mutedVideo]);
   
   const toggleAudio = useCallback(() => {
    callObject!.setLocalAudio(mutedAudio);
   }, [callObject, mutedAudio]);

   const toggleMeetingInformation = () => {
    showMeetingInformation
      ? setShowMeetingInformation(false)
      : setShowMeetingInformation(true);
  };

  return render()
}

export default Tray