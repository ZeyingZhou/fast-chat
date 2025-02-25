# Real-Time Messenger Application

A modern, real-time messenger application built with Next.js, FastAPI, DynamoDB, and AWS S3. The application features real-time messaging, file sharing, authentication, and more.

## Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe code
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Reusable UI components
- **Zustand** - State management
- **Lucide React** - Icon library

### Backend
- **FastAPI** - Python API framework
- **WebSockets** - Real-time communication
- **Pydantic** - Data validation

### Authentication
- **Clerk** - Authentication service
- **Webhook integration** - User data synchronization

### Database & Storage
- **DynamoDB** - NoSQL database
- **AWS S3** - Object storage for media files

## Features

- **Real-time messaging** using WebSockets
- **User authentication** via Clerk
- **Multiple file uploads** support for images and documents
- **Message read receipts**
- **User profile management**
- **Responsive design** for mobile and desktop
- **Dark mode support**
- **Direct S3 uploads** using presigned URLs

## Architecture

The application follows a modern architecture with separate frontend and backend services:

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Next.js   │◄────┤   FastAPI    │◄────┤  DynamoDB   │
│  Frontend   │────►│   Backend    │────►│  Database   │
└─────────────┘     └──────────────┘     └─────────────┘
       │                    │                    
       │               ┌────▼───────┐            
       └──────────────►│   AWS S3    │            
                       │  Storage    │            
                       └────────────┘            
       ┌─────────────┐      │                    
       │   Clerk     │      │                    
       │   Auth      │──────┘                    
       └─────────────┘                           
       │        ▲
       │        │
       └────────┘
```

### Data Flow

1. **Authentication**:
   - Users authenticate via Clerk in the frontend
   - Clerk webhooks notify FastAPI of user events
   - FastAPI syncs user data to DynamoDB

2. **Messaging**:
   - Messages are sent from frontend to FastAPI
   - FastAPI saves to DynamoDB and broadcasts via WebSocket

3. **File Uploads**:
   - Frontend requests presigned URL from FastAPI
   - Files are uploaded directly to S3 using the presigned URL
   - File URLs are stored with messages in DynamoDB

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.9+
- AWS Account (for DynamoDB and S3)
- Clerk Account

### Environment Variables

#### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
CLERK_SECRET_KEY=your_clerk_secret_key
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/
```

#### Backend (.env)
```
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_aws_region
AWS_BUCKET_NAME=your_s3_bucket_name
CLERK_SECRET_KEY=your_clerk_secret_key
WEBHOOK_SECRET=your_webhook_secret
ORIGINS=http://localhost:3000
```

### Installation

#### Frontend
```bash
# Clone the repository
git clone https://github.com/yourusername/messenger-clone.git
cd messenger-clone/frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

#### Backend
```bash
# Navigate to backend directory
cd ../backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

### Setting up Clerk Webhooks

1. Go to Clerk Dashboard
2. Navigate to Webhooks
3. Add a new webhook with URL: `https://your-api-url/api/webhooks/clerk`
4. Select events:
   - user.created
   - user.updated
   - user.deleted
5. Copy the signing secret to your backend .env file

### AWS Configuration

1. Create an S3 bucket with appropriate CORS settings:
```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["PUT", "GET"],
    "AllowedOrigins": ["http://localhost:3000"],
    "ExposeHeaders": []
  }
]
```

2. Set up DynamoDB tables:
   - users
   - conversations
   - messages
   - conversation_users

## Deployment

### Frontend (Vercel)
```bash
# Build the application
npm run build

# Deploy to Vercel
vercel
```

### Backend (AWS, Heroku, etc.)
```bash
# Build Docker image
docker build -t messenger-backend .

# Deploy to your preferred platform
# AWS ECS, Heroku, etc.
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Clerk Documentation](https://clerk.dev/docs)
- [AWS SDK Documentation](https://docs.aws.amazon.com/sdk-for-javascript/index.html)
