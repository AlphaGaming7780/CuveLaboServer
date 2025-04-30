import React, { useContext, useState, useRef } from 'react';
import './RegisteredUserPanel.css';
import { ChangeClientMode, ResetActiveClient, TakeControl, UpdatedClientDataContext } from '../API/ClientAPI.tsx';
import { RadioCheckbox } from './RadioCheckbox/RadioCheckbox.tsx';
import { ClientPanel } from './ClientPanel/ClientPanel.tsx';
import { IsAdminContext, RegisterAdmin } from '../API/Admin.tsx';

export const RegisteredUserPanel = () => {

	const { ClientEnabled, ActiveClient, ClientList } = useContext(UpdatedClientDataContext)
	const IsAdmin = useContext(IsAdminContext)

	const passwordInputRef = useRef(null);
	const usernameInputRef = useRef(null);

	return (
		<div className="registered-user-panel">
			<h3>Admin Panel</h3>
			{IsAdmin ? <>
				<div style={{display:"flex", flexDirection:"row", alignItems:"center"}}>
					<button type='button' onClick={ () => ResetActiveClient() } >Reset Clients</button>
					<button type='button' onClick={ () => TakeControl() } >Take control</button>
				</div>
				<span style={{display:"flex", flexDirection:"row", alignItems:"center"}}>
					<RadioCheckbox checked={ClientEnabled} onChange={ChangeClientMode} />
					<p style={{paddingLeft: "0.4rem" }}>Disable/Enable clients (students)</p>
				</span>	
			</> : <>
				<span style={{display:"flex", flexDirection:"collum", alignItems:"center"}}>
					<input ref={usernameInputRef} type='text' placeholder='Username (optional)'/>
					<input ref={passwordInputRef} type='password' placeholder='Password' style={{paddingTop: "0.4rem" }} />
					<button onClick={ () => {RegisterAdmin(passwordInputRef.value, usernameInputRef.value)}} style={{paddingTop: "0.4rem" }} >Register</button>
				</span>	
			</>
			}

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
