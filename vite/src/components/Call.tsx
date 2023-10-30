import { DailyVideo, useActiveSpeakerId, useDaily, useLocalParticipant, useParticipant, useParticipantIds } from '@daily-co/daily-react';
import React from 'react';
import Tile from './Tile';

const Call = () => {
  const callObject = useDaily();
  const activeSpeakerId = useActiveSpeakerId();
  const remoteParticipantIds = useParticipantIds({ filter: 'remote' });
  const localParticipant = useLocalParticipant();
  const activeSpeaker = useParticipant(activeSpeakerId || localParticipant!.user_id)
  function render() {
    return(
        <div className="flex gap-6">
          <div className={`
            rounded-lg overflow-hidden relative
            ${activeSpeakerId === localParticipant?.user_id ? 'border-4 border-yellow-600 border-solid' : 'border-4 border-transparent'}`}>
            {activeSpeaker &&  
              <DailyVideo sessionId={activeSpeaker.session_id} mirror type="video" />
            }
            <span className="absolute bottom-1 left-1 text-white bg-gray-800 text-sm px-2 py-1.5 bg-opacity-90">
              {activeSpeaker?.user_name}
            </span>
          </div>
          <div className="flex gap-6 flex-col">
            {remoteParticipantIds.map((id) => (
              <Tile key={id} id={id} isScreenShare={false} />
            ))}
          </div>
        </div>
    )
  }

  return render()
}

export default Call