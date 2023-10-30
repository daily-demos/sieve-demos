import { useCallback, useEffect, useState } from 'react'
import { DailyProvider } from '@daily-co/daily-react'
import HairCheck from './HairCheck'
import Call from './Call';
import Tray from './Tray';
import DailyIframe, { DailyCall, DailyEvent } from '@daily-co/daily-js';

export const DAILY_URL = "https://sexton.daily.co/howdy";
type CallStatus = "SHOW_HAIRCHECK" | "SHOW_CALL" | "ERROR" | "LEAVING";

function DailyCall() {
  const [callObject, setCallObject] = useState<DailyCall | null>()
  const [callStatus, setCallStatus] = useState<CallStatus>("SHOW_HAIRCHECK")

  useEffect(() => {
    if (callStatus === "SHOW_HAIRCHECK") {
      const call = DailyIframe.createCallObject({ url: DAILY_URL });
      setCallObject(call);
      call.startCamera();
    }
  }, [callStatus]);

  function render() {
    if (!callObject) return;
    switch(callStatus) {
      case "SHOW_HAIRCHECK":
        return(
          <DailyProvider callObject={callObject}>
            <HairCheck />
          </DailyProvider>
        )
      case "SHOW_CALL":
        return(
          <DailyProvider callObject={callObject}>
            <div className="flex flex-col min-h-[100vh]">
              <div className="flex-1 flex items-center justify-center bg-gray-800">
                <Call/>
              </div>
              <Tray leaveCall={startLeavingCall}/>
            </div>
          </DailyProvider>
        )
    }
  }

  function handleNewMeetingState() {
    if (!callObject) return;
    switch (callObject.meetingState()) {
      case 'joined-meeting':
        // transcription.startTranscription();
        setCallStatus("SHOW_CALL");
        break;
      case 'left-meeting':
        callObject.destroy().then(() => {
          setCallObject(null);
          setCallStatus("SHOW_CALL");
        });
        break;
      case 'error':
        setCallStatus("ERROR");
        break;
      default:
        break;
    }
  }

  useEffect(() => {
    if (!callObject) return;

    const events: DailyEvent[] = ['joined-meeting', 'left-meeting', 'error', 'camera-error'];
    handleNewMeetingState();

    events.forEach((event) => callObject.on(event, handleNewMeetingState));

    // Stop listening for changes in state
    return () => {
      events.forEach((event) => callObject.off(event, handleNewMeetingState));
    };
  }, [callObject]);


    const startLeavingCall = useCallback(() => {
      if (!callObject) return;
      setCallStatus("LEAVING");
      callObject.leave();
    }, [callObject, callStatus]);

  return render();
}



export default DailyCall
