import { DailyVideo, useDaily, useDevices, useLocalParticipant } from '@daily-co/daily-react';
import { SyntheticEvent } from 'react';
import { DAILY_URL } from '../App';

const HairCheck = () => {
  const callObject = useDaily();
  const localParticipant = useLocalParticipant();
  const { microphones, speakers, cameras, setMicrophone, setCamera, setSpeaker } = useDevices();

  function render() {
    if (!callObject) return;
    return(
      <form onSubmit={joinCall}>
        {localParticipant && <DailyVideo sessionId={localParticipant.session_id} mirror type="video" />}
        <div>
          <label htmlFor="username">Your name:</label>
          <input
            name="username"
            type="text"
            placeholder="Enter username"
            onChange={(e) => callObject.setUserName(e.target.value)}
            value={localParticipant?.user_name || ' '}
          />
        </div>
        <div>
          <label htmlFor="cameraOptions">Camera:</label>
          <select name="cameraOptions" id="cameraSelect" onChange={(e) => setCamera(e.target.value)}>
            {cameras?.map((camera) => (
              <option key={`cam-${camera.device.deviceId}`} value={camera.device.deviceId}>
                {camera.device.label}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="micOptions">Microphone:</label>
          <select name="micOptions" id="micSelect" onChange={(e) => setMicrophone(e.target.value)}>
            {microphones?.map((mic) => (
              <option key={`mic-${mic.device.deviceId}`} value={mic.device.deviceId}>
                {mic.device.label}
              </option>
            ))}
          </select>
        </div>
        
        <div>
          <label htmlFor="speakersOptions">Speakers:</label>
          <select name="speakersOptions" id="speakersSelect" onChange={(e) => setSpeaker(e.target.value)}>
            {speakers?.map((speaker) => (
              <option key={`speaker-${speaker.device.deviceId}`} value={speaker.device.deviceId}>
                {speaker.device.label}
              </option>
            ))}
          </select>
        </div>

        <div>
        <button onClick={(e) => joinCall(e)} type="submit">Join call</button>
        </div>
      </form>
    )
  }

  const joinCall = (e:SyntheticEvent) => {
    e.preventDefault();
    if (!callObject) return;
    callObject.join({ url: DAILY_URL });
  }

  return render()
}

export default HairCheck