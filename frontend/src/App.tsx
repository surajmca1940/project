import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';
import { Provider } from 'react-redux';
import { QueryClient, QueryClientProvider } from 'react-query';
import { HelmetProvider } from 'react-helmet-async';

import { store } from './store/store';
import { SocketProvider } from './hooks/useSocket';
import { AuthProvider } from './hooks/useAuth';

// Layout Components
import Header from './components/common/Header';
import Sidebar from './components/common/Sidebar';
import Footer from './components/common/Footer';
import LoadingScreen from './components/common/LoadingScreen';
import ErrorBoundary from './components/common/ErrorBoundary';

// Page Components
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import AISupportPage from './pages/AISupportPage';
import BookingPage from './pages/BookingPage';
import ResourcesPage from './pages/ResourcesPage';
import PeerSupportPage from './pages/PeerSupportPage';
import AdminDashboardPage from './pages/AdminDashboardPage';
import ProfilePage from './pages/ProfilePage';
import NotFoundPage from './pages/NotFoundPage';

// Create theme
const theme = createTheme({
  palette: {
    primary: {
      main: process.env.REACT_APP_THEME_PRIMARY_COLOR || '#1976d2',
    },
    secondary: {
      main: process.env.REACT_APP_THEME_SECONDARY_COLOR || '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 600,
    },
    h2: {
      fontWeight: 600,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        },
      },
    },
  },
});

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      staleTime: 1000 * 60 * 5, // 5 minutes
    },
  },
});

const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <HelmetProvider>
        <Provider store={store}>
          <QueryClientProvider client={queryClient}>
            <ThemeProvider theme={theme}>
              <CssBaseline />
              <SocketProvider>
                <AuthProvider>
                  <Router>
                    <Box
                      sx={{
                        display: 'flex',
                        flexDirection: 'column',
                        minHeight: '100vh',
                      }}
                    >
                      <Header />
                      <Box sx={{ display: 'flex', flex: 1 }}>
                        <Sidebar />
                        <Box
                          component="main"
                          sx={{
                            flexGrow: 1,
                            p: 3,
                            backgroundColor: 'background.default',
                          }}
                        >
                          <Routes>
                            {/* Public Routes */}
                            <Route path="/" element={<HomePage />} />
                            <Route path="/login" element={<LoginPage />} />
                            <Route path="/register" element={<RegisterPage />} />
                            
                            {/* Protected Routes */}
                            <Route path="/dashboard" element={<DashboardPage />} />
                            <Route path="/ai-support" element={<AISupportPage />} />
                            <Route path="/booking" element={<BookingPage />} />
                            <Route path="/resources" element={<ResourcesPage />} />
                            <Route path="/peer-support" element={<PeerSupportPage />} />
                            <Route path="/profile" element={<ProfilePage />} />
                            
                            {/* Admin Routes */}
                            <Route path="/admin" element={<AdminDashboardPage />} />
                            
                            {/* Catch All Route */}
                            <Route path="/404" element={<NotFoundPage />} />
                            <Route path="*" element={<Navigate to="/404" replace />} />
                          </Routes>
                        </Box>
                      </Box>
                      <Footer />
                    </Box>
                  </Router>
                </AuthProvider>
              </SocketProvider>
            </ThemeProvider>
          </QueryClientProvider>
        </Provider>
      </HelmetProvider>
    </ErrorBoundary>
  );
};

export default App;
