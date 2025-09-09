import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Paper,
  TextField,
  IconButton,
  Typography,
  Avatar,
  Chip,
  CircularProgress,
  Alert,
  Button,
} from '@mui/material';
import {
  Send as SendIcon,
  SmartToy as BotIcon,
  Person as PersonIcon,
  Warning as WarningIcon,
  Support as SupportIcon,
} from '@mui/icons-material';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  sentiment?: 'positive' | 'negative' | 'neutral' | 'concerning';
  riskLevel?: 'low' | 'medium' | 'high' | 'critical';
}

interface ChatInterfaceProps {
  sessionId?: string;
  onEscalation?: () => void;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ sessionId, onEscalation }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m here to provide mental health support and guidance. How are you feeling today?',
      timestamp: new Date(),
      sentiment: 'positive',
      riskLevel: 'low',
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showCrisisAlert, setShowCrisisAlert] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Simulate API call to backend
      const response = await fetch('/api/chat/message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({
          sessionId: sessionId || 'default',
          message: userMessage.content,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const data = await response.json();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
        sentiment: data.sentiment,
        riskLevel: data.riskLevel,
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Check for crisis situations
      if (data.riskLevel === 'critical' || data.needsEscalation) {
        setShowCrisisAlert(true);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'I apologize, but I\'m having trouble responding right now. Please try again or contact support if the issue persists.',
        timestamp: new Date(),
        sentiment: 'neutral',
        riskLevel: 'low',
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  const getRiskLevelColor = (riskLevel?: string) => {
    switch (riskLevel) {
      case 'critical': return 'error';
      case 'high': return 'warning';
      case 'medium': return 'info';
      default: return 'success';
    }
  };

  const handleContactCounselor = () => {
    if (onEscalation) {
      onEscalation();
    }
    // Navigate to booking page or show contact information
  };

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Crisis Alert */}
      {showCrisisAlert && (
        <Alert
          severity="error"
          icon={<WarningIcon />}
          action={
            <Button
              color="inherit"
              size="small"
              onClick={handleContactCounselor}
              startIcon={<SupportIcon />}
            >
              Contact Counselor
            </Button>
          }
          sx={{ mb: 2 }}
        >
          I'm concerned about your wellbeing. Please consider speaking with a professional counselor.
          <br />
          <strong>Crisis Hotline: {process.env.REACT_APP_CRISIS_HOTLINE}</strong>
        </Alert>
      )}

      {/* Messages Container */}
      <Paper
        sx={{
          flex: 1,
          p: 2,
          mb: 2,
          maxHeight: '60vh',
          overflowY: 'auto',
          backgroundColor: '#fafafa',
        }}
      >
        {messages.map((message) => (
          <Box
            key={message.id}
            sx={{
              display: 'flex',
              mb: 2,
              justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
            }}
          >
            {message.role === 'assistant' && (
              <Avatar sx={{ mr: 1, bgcolor: 'primary.main' }}>
                <BotIcon />
              </Avatar>
            )}
            
            <Box
              sx={{
                maxWidth: '70%',
                order: message.role === 'user' ? 0 : 1,
              }}
            >
              <Paper
                sx={{
                  p: 2,
                  bgcolor: message.role === 'user' ? 'primary.main' : 'white',
                  color: message.role === 'user' ? 'white' : 'text.primary',
                }}
              >
                <Typography variant="body1">{message.content}</Typography>
                <Typography
                  variant="caption"
                  sx={{
                    display: 'block',
                    mt: 1,
                    opacity: 0.7,
                  }}
                >
                  {message.timestamp.toLocaleTimeString()}
                </Typography>
              </Paper>
              
              {/* Show risk level for assistant messages */}
              {message.role === 'assistant' && message.riskLevel && (
                <Box sx={{ mt: 1, display: 'flex', gap: 1 }}>
                  <Chip
                    label={`Risk: ${message.riskLevel}`}
                    size="small"
                    color={getRiskLevelColor(message.riskLevel) as any}
                    variant="outlined"
                  />
                  {message.sentiment && (
                    <Chip
                      label={`Mood: ${message.sentiment}`}
                      size="small"
                      variant="outlined"
                    />
                  )}
                </Box>
              )}
            </Box>

            {message.role === 'user' && (
              <Avatar sx={{ ml: 1, bgcolor: 'secondary.main' }}>
                <PersonIcon />
              </Avatar>
            )}
          </Box>
        ))}
        
        {isLoading && (
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Avatar sx={{ mr: 1, bgcolor: 'primary.main' }}>
              <BotIcon />
            </Avatar>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <CircularProgress size={20} sx={{ mr: 1 }} />
              <Typography variant="body2" color="text.secondary">
                AI is typing...
              </Typography>
            </Box>
          </Box>
        )}
        
        <div ref={messagesEndRef} />
      </Paper>

      {/* Input Area */}
      <Box sx={{ display: 'flex', gap: 1 }}>
        <TextField
          fullWidth
          multiline
          maxRows={4}
          placeholder="Type your message here..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isLoading}
          variant="outlined"
        />
        <IconButton
          color="primary"
          onClick={handleSendMessage}
          disabled={!inputValue.trim() || isLoading}
          sx={{
            bgcolor: 'primary.main',
            color: 'white',
            '&:hover': {
              bgcolor: 'primary.dark',
            },
          }}
        >
          <SendIcon />
        </IconButton>
      </Box>

      {/* Disclaimer */}
      <Typography
        variant="caption"
        color="text.secondary"
        sx={{ mt: 1, textAlign: 'center' }}
      >
        This AI assistant provides general support. For emergencies, please contact emergency services
        or call {process.env.REACT_APP_CRISIS_HOTLINE}
      </Typography>
    </Box>
  );
};

export default ChatInterface;
