# Insta485: Client-Side Web Application

This project is a client-side web application that replicates the core functionality of Instagram.  
It was built as part of EECS 485 at the University of Michigan.

## Features
- Responsive, single-page application (SPA) built with JavaScript, HTML, and CSS
- Dynamic photo feed with infinite scrolling
- User authentication and session management (login, logout, registration)
- Profile pages with user posts and follower/following counts
- Follow and unfollow other users
- Like and comment on posts
- RESTful API integration with a backend server

## Technologies Used
- JavaScript (ES6+)
- HTML5
- CSS3
- REST API (provided backend)
- Webpack (build tool)
- Babel (JavaScript compiler)

## Getting Started

### Prerequisites
- Node.js and npm installed

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/insta485-clientside.git
    cd insta485-clientside
    ```

2. Install dependencies:
    ```bash
    npm install
    ```

3. Build the project:
    ```bash
    npm run build
    ```

4. Start the backend server (provided separately) and serve the static files from `dist/`.

### Development
To start a live-reloading development server:
```bash
npm start
