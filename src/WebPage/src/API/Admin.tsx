import React, { createContext, use, useEffect, useState } from "react";
import { PostData } from "./PostData.tsx";

interface AdminRequest {
    MDP : string;
}

let adminRequest : AdminRequest | null = null;
let SetDirty 

// Create a Context
export const IsAdminContext = createContext(false);

export const IsAdminContextProvider = ({ children }) => {

    const [isAdmin, setIsAdmin] = useState(false);
    const [Dirty, setDirty] = useState(false);

    SetDirty = setDirty;

    useEffect(() => {
        const fetchData = async (mdp : string) => {
            let succes = true;
            try {
                await PostData<AdminRequest>("/IsAdmin", { MDP: mdp });
            } catch (error) {
                console.error("Erreur lors du fetch de IsAdmin:", error.message);
                succes = false;
            } 

            if(succes) {
                setIsAdmin(true);
            }

            adminRequest = null; // Reset adminRequest after use

        };

        if(Dirty && adminRequest !== null) {
            fetchData(adminRequest.MDP);
        } 
    }, [Dirty]);

    return (
      <IsAdminContext.Provider value={ isAdmin }>
        {children}
      </IsAdminContext.Provider>
    );
};

export const RegisterAdmin = (MDP : string) => {
    adminRequest = {MDP: MDP};
    SetDirty();
}