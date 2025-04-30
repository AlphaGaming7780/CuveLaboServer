// https://stackoverflow.com/questions/70711842/how-to-get-my-system-local-ip-using-react-js

import os from 'os';

const getLocalIP = () => {
  const interfaces = os.networkInterfaces();
  for (const name of Object.keys(interfaces)) {
    for (const iface of interfaces[name]) {
      if (iface.family === 'IPv4' && !iface.internal) {
        return iface.address;
      }
    }
  }
  return null;
};

export default getLocalIP;