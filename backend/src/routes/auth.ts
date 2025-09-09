import express from 'express';
import jwt from 'jsonwebtoken';
import { body, validationResult } from 'express-validator';
import User from '../models/User';
import { logger } from '../config/logger';

const router = express.Router();

// Register endpoint
router.post('/register',
  [
    body('email').isEmail().normalizeEmail(),
    body('password').isLength({ min: 6 }),
    body('name').isLength({ min: 2 }).trim(),
    body('role').optional().isIn(['student', 'counselor', 'admin', 'volunteer']),
    body('institution').optional().isLength({ min: 2 }).trim(),
  ],
  async (req, res) => {
    try {
      // Check for validation errors
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          message: 'Validation failed',
          errors: errors.array()
        });
      }

      const { email, password, name, role, institution, department, year } = req.body;

      // Check if user already exists
      const existingUser = await User.findOne({ email });
      if (existingUser) {
        return res.status(400).json({
          message: 'User already exists with this email'
        });
      }

      // Create new user
      const user = new User({
        email,
        passwordHash: password, // Will be hashed by pre-save middleware
        profile: {
          name,
          role: role || 'student',
          institution,
          department,
          year,
          preferences: {
            language: 'en',
            notifications: true,
            privacy: {
              shareAnalytics: true,
              allowPeerSupport: true
            }
          }
        }
      });

      await user.save();

      // Generate JWT token
      const token = jwt.sign(
        { userId: user._id, email: user.email },
        process.env.JWT_SECRET!,
        { expiresIn: process.env.JWT_EXPIRE || '24h' }
      );

      logger.info(`User registered: ${user.email}`);

      res.status(201).json({
        message: 'User registered successfully',
        token,
        user: {
          id: user._id,
          email: user.email,
          profile: user.profile
        }
      });
    } catch (error) {
      logger.error('Registration error:', error);
      res.status(500).json({
        message: 'Internal server error'
      });
    }
  }
);

// Login endpoint
router.post('/login',
  [
    body('email').isEmail().normalizeEmail(),
    body('password').exists(),
  ],
  async (req, res) => {
    try {
      // Check for validation errors
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          message: 'Validation failed',
          errors: errors.array()
        });
      }

      const { email, password } = req.body;

      // Find user by email
      const user = await User.findOne({ email });
      if (!user) {
        return res.status(401).json({
          message: 'Invalid email or password'
        });
      }

      // Check if user is active
      if (!user.isActive) {
        return res.status(401).json({
          message: 'Account is deactivated. Please contact support.'
        });
      }

      // Verify password
      const isPasswordValid = await user.comparePassword(password);
      if (!isPasswordValid) {
        return res.status(401).json({
          message: 'Invalid email or password'
        });
      }

      // Update last login
      user.lastLogin = new Date();
      await user.save();

      // Generate JWT token
      const token = jwt.sign(
        { userId: user._id, email: user.email, role: user.profile.role },
        process.env.JWT_SECRET!,
        { expiresIn: process.env.JWT_EXPIRE || '24h' }
      );

      logger.info(`User logged in: ${user.email}`);

      res.json({
        message: 'Login successful',
        token,
        user: {
          id: user._id,
          email: user.email,
          profile: user.profile,
          lastLogin: user.lastLogin
        }
      });
    } catch (error) {
      logger.error('Login error:', error);
      res.status(500).json({
        message: 'Internal server error'
      });
    }
  }
);

// Refresh token endpoint
router.post('/refresh',
  async (req, res) => {
    try {
      const { token } = req.body;

      if (!token) {
        return res.status(401).json({
          message: 'Refresh token is required'
        });
      }

      // Verify the refresh token
      const decoded = jwt.verify(token, process.env.JWT_SECRET!) as any;
      
      // Find user
      const user = await User.findById(decoded.userId);
      if (!user || !user.isActive) {
        return res.status(401).json({
          message: 'Invalid refresh token'
        });
      }

      // Generate new access token
      const newToken = jwt.sign(
        { userId: user._id, email: user.email, role: user.profile.role },
        process.env.JWT_SECRET!,
        { expiresIn: process.env.JWT_EXPIRE || '24h' }
      );

      res.json({
        message: 'Token refreshed successfully',
        token: newToken
      });
    } catch (error) {
      logger.error('Token refresh error:', error);
      res.status(401).json({
        message: 'Invalid refresh token'
      });
    }
  }
);

// Logout endpoint (optional - mainly for logging)
router.post('/logout',
  async (req, res) => {
    try {
      const authHeader = req.headers.authorization;
      if (authHeader) {
        const token = authHeader.split(' ')[1];
        const decoded = jwt.verify(token, process.env.JWT_SECRET!) as any;
        logger.info(`User logged out: ${decoded.email}`);
      }

      res.json({
        message: 'Logout successful'
      });
    } catch (error) {
      // Even if token verification fails, we still return success
      res.json({
        message: 'Logout successful'
      });
    }
  }
);

// Password reset request
router.post('/forgot-password',
  [
    body('email').isEmail().normalizeEmail(),
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          message: 'Please provide a valid email address',
          errors: errors.array()
        });
      }

      const { email } = req.body;
      
      const user = await User.findOne({ email });
      if (!user) {
        // Don't reveal if user exists or not for security
        return res.json({
          message: 'If an account with that email exists, we have sent a password reset link'
        });
      }

      // Generate password reset token (implement this based on your needs)
      const resetToken = jwt.sign(
        { userId: user._id, purpose: 'password-reset' },
        process.env.JWT_SECRET!,
        { expiresIn: '1h' }
      );

      // TODO: Send email with reset link
      // await sendPasswordResetEmail(user.email, resetToken);

      logger.info(`Password reset requested for: ${user.email}`);

      res.json({
        message: 'If an account with that email exists, we have sent a password reset link'
      });
    } catch (error) {
      logger.error('Password reset error:', error);
      res.status(500).json({
        message: 'Internal server error'
      });
    }
  }
);

export default router;
