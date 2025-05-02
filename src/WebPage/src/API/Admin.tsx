import React, { createContext, useEffect, useState } from "react";
import { PostData } from "./PostData.tsx";

interface AdminRequest {
    Password : string;
    Name? : string;
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
        const fetchData = async (adminRequest : AdminRequest) => {
            let succes = true;
            try {
                await PostData<AdminRequest>("/RegisterAdmin", adminRequest);
            } catch (error) {
                console.error("Erreur lors du fetch de IsAdmin:", error.message);
                succes = false;
            } 

            if(succes) {
                setIsAdmin(true);
            }

        };

        if(Dirty && adminRequest !== null) {
            setDirty(false); // Reset Dirty after use
            fetchData(adminRequest);
            adminRequest = null; // Reset adminRequest after use
        } 
    }, [Dirty]);

    return (
      <IsAdminContext.Provider value={ isAdmin }>
        {children}
      </IsAdminContext.Provider>
    );
};

export const RegisterAdmin = (password : string, name? : string) => {
    adminRequest = {Password: password, Name: name};
    SetDirty(true);
}