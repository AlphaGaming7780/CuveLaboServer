import React, { useContext } from 'react';
import './RegisteredUserPanel.css';
import { ChangeClientMode, ResetActiveClient, TakeControl, UpdatedClientDataContext } from '../API/ClientAPI.tsx';
import { RadioCheckbox } from './RadioCheckbox/RadioCheckbox.tsx';
import { ClientPanel } from './ClientPanel/ClientPanel.tsx';

export const RegisteredUserPanel = () => {

	const { ClientEnabled, ActiveClient, ClientList } = useContext(UpdatedClientDataContext)

	return (
		<div className="registered-user-panel">
			<h2>Registered User Panel</h2>
			<div style={{display:"flex", flexDirection:"row", alignItems:"center"}}>
				<button type='button' onClick={ () => ResetActiveClient() } >Reset Clients</button>
				<button type='button' onClick={ () => TakeControl() } >Take control</button>
			</div>
			<span style={{display:"flex", flexDirection:"row", alignItems:"center"}}>
				<RadioCheckbox checked={ClientEnabled} onChange={ChangeClientMode} />
				<p style={{paddingLeft: "0.4rem" }}>Disable/Enable</p>
			</span>

			<h3>Active Client</h3>
			<ClientPanel client={ActiveClient} />

			<div className='clientList'>
				<h3>Client List</h3>
				{ClientList.map((client, index) => (
						<ClientPanel index={index} client={client} />
				))}
			</div>
		</div> 
	);
}
