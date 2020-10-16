#!/bin/bash

cd /frontend/

# Starting the frontend after building deps
npm install
npm run build
npm start
