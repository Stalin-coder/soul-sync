# Soul Sync

Soul Sync is a voice-enabled, engagement-aware learning companion designed to improve motivation and understanding in self-paced online learning environments.

## Problem Statement
Many online learning platforms deliver static content and feedback, which fails to adapt to individual learner engagement. This often leads to confusion, frustration, and dropout—especially for beginners without access to personalized guidance.

## Solution Overview
Soul Sync adapts explanations and feedback based on learner engagement inferred from interaction behavior and text sentiment derived from voice input. The system focuses on ethical, non-biometric AI to provide personalized learning support without invasive data collection.

## Key Features
- Voice-based learner interaction  
- Speech-to-text processing  
- Text-based sentiment analysis using NLP  
- Engagement-aware adaptive feedback  
- Ethical and privacy-first design  
- Web-based application built with Flask  

## Technologies Used
- Python  
- Flask (Backend Web Framework)  
- Google Cloud Natural Language API (Sentiment Analysis)  
- HTML, CSS, JavaScript  

## How It Works
1. Learner interacts with the system using voice input  
2. Voice input is converted into text  
3. Text sentiment is analyzed using Google Cloud Natural Language API  
4. Learner engagement level is inferred  
5. Feedback and explanation depth are adapted accordingly  
6. Personalized response is delivered to the learner  

## Architecture Overview
User → Flask Web Application → Speech-to-Text Module →  
Google Cloud Natural Language API → Engagement Analyzer →  
Adaptive Feedback Engine → Learner Output

## Demo
A working demonstration of the MVP is available in the project demo video:
- YouTube Demo: <PASTE YOUR YOUTUBE LINK HERE>

## Project Status
This project is a functional MVP developed as a solo submission for hackathons. Future improvements include multilingual support, learning analytics, and enhanced voice interaction.

## Author
Developed by a solo undergraduate student from  
Sri Venkateswara College of Engineering.
