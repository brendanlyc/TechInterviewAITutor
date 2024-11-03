import { BrowserRouter, Route, Routes } from 'react-router-dom';
import './App.css';
import { AuthProvider } from './context/AuthContext';
import HomePage from './pages/HomePage/HomePage'
import LoginPage from './pages/authentication/LoginPage/LoginPage'
import CreateAccountPage from './pages/authentication/CreateAccountPage/CreateAccountPage';
import ResetPasswordPage from './pages/authentication/ResetPasswordPage/ResetPasswordPage';
import ResetPasswordRequestPage from './pages/authentication/ResetPasswordRequestPage/ResetPasswordRequestPage';
import ContentPage from './pages/ContentPage/ContentPage';
import Settings from './pages/Settings/Settings';
import PrivateRoute from './PrivateRoute';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Authentication routes */}
          <Route path="/" element={<LoginPage />} />
          <Route path="/create-account" element={<CreateAccountPage />} />
          <Route path="/reset-password" element={<ResetPasswordRequestPage />} />
          <Route path="/reset-password/:userId/:token" element={<ResetPasswordPage />} />

          {/* Main application routes */}

          <Route 
            path="/home"
            // element={
            //   <PrivateRoute>
            //     <HomePage />
            //   </PrivateRoute>
            // }
            element={<HomePage />}
          />

          <Route 
            path="/settings"
            // element={
            //   <PrivateRoute>
            //     <Settings />
            //   </PrivateRoute>
            // }
            element={<Settings />}
          />

          <Route 
            path="/content/:userId/:title"
            // element={
            //   <PrivateRoute>
            //     <ContentPage />
            //   </PrivateRoute>
            // }
            element={<ContentPage />}
          />

        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App;
