import React, { useContext, useState } from 'react';
import './RegisteredUserPanel.css';
import { ChangeClientMode, ResetActiveClient, TakeControl, UpdatedClientDataContext } from '../API/ClientAPI.tsx';
import { RadioCheckbox } from './RadioCheckbox/RadioCheckbox.tsx';
import { ClientPanel } from './ClientPanel/ClientPanel.tsx';
import { IsAdminContext, RegisterAdmin } from '../API/Admin.tsx';

export const RegisteredUserPanel = () => {

	const { ClientEnabled, ActiveClient, ClientList } = useContext(UpdatedClientDataContext)
	const IsAdmin = useContext(IsAdminContext)

	const [password, setPassword] = useState("")

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
				<span style={{display:"flex", flexDirection:"row", alignItems:"center"}}>
					<input onChange={ (i) => {setPassword(i.target.value)}} type='password' placeholder='Password'>Password</input>
					<button onClick={ () => RegisterAdmin(password)} style={{paddingLeft: "0.4rem" }} >Register</button>
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
