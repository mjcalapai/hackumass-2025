Directions to start the game on local host.  

Make sure the machine has:  
- Python 3.10+  

- Node.js 18+ (or reasonably recent)  

- npm  

1. Backend startup  
- Install the following if needed with the command below  
   pip install fastapi uvicorn pydantic  
- After the install, you may run:  
   uvicorn midleware.server:app --reload  

- Successful output will look like the following:
\hackumass-2025> uvicorn midleware.server:app --reload  
INFO:     Will watch for changes in these directories: ['C:\\Users\\mitch\\SoftwareEngineering\\hackumass-2025']  
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)  
INFO:     Started reloader process [39216] using StatReload  
[INIT] Placed 26 pieces on the board.  
INFO:     Started server process [53176]  
INFO:     Waiting for application startup.  
INFO:     Application startup complete.  




2. Front end startup:  
   - Only do so after starting the backend  
   - Open a new terminal, do now kill the backend and navigate to the frontend directory. Run the following commands:  

     cd hackumass-2025/frontend  
     npm install  
     npm run dev  


  - A success will output:  
    \hackumass-2025\frontend> npm run dev  

> frontend@0.0.0 dev  
> vite  


  VITE v#  ready in ## ms  

  ➜  Local:   http://localhost:5173/  
  ➜  Network: use --host to expose  
  ➜  press h + enter to show help  




- You may now open the local host  

- I hope you enjoy!  
