import mongoose, { Document, Schema } from 'mongoose';
import bcrypt from 'bcryptjs';

export interface IUser extends Document {
  email: string;
  passwordHash: string;
  profile: {
    name: string;
    role: 'student' | 'counselor' | 'admin' | 'volunteer';
    institution?: string;
    department?: string;
    year?: number;
    preferences: {
      language: string;
      notifications: boolean;
      privacy: {
        shareAnalytics: boolean;
        allowPeerSupport: boolean;
      };
    };
  };
  isActive: boolean;
  emailVerified: boolean;
  lastLogin?: Date;
  createdAt: Date;
  updatedAt: Date;
  comparePassword(candidatePassword: string): Promise<boolean>;
}

const UserSchema = new Schema<IUser>({
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    trim: true,
    match: [/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/, 'Please enter a valid email']
  },
  passwordHash: {
    type: String,
    required: true,
    minlength: 6
  },
  profile: {
    name: {
      type: String,
      required: true,
      trim: true,
      maxlength: 100
    },
    role: {
      type: String,
      enum: ['student', 'counselor', 'admin', 'volunteer'],
      default: 'student'
    },
    institution: {
      type: String,
      trim: true,
      maxlength: 200
    },
    department: {
      type: String,
      trim: true,
      maxlength: 100
    },
    year: {
      type: Number,
      min: 1,
      max: 8
    },
    preferences: {
      language: {
        type: String,
        default: 'en',
        enum: ['en', 'hi', 'bn', 'te', 'ta', 'mr', 'gu', 'kn', 'ml', 'pa']
      },
      notifications: {
        type: Boolean,
        default: true
      },
      privacy: {
        shareAnalytics: {
          type: Boolean,
          default: true
        },
        allowPeerSupport: {
          type: Boolean,
          default: true
        }
      }
    }
  },
  isActive: {
    type: Boolean,
    default: true
  },
  emailVerified: {
    type: Boolean,
    default: false
  },
  lastLogin: {
    type: Date
  }
}, {
  timestamps: true,
  collection: 'users'
});

// Index for better query performance
UserSchema.index({ email: 1 });
UserSchema.index({ 'profile.role': 1 });
UserSchema.index({ 'profile.institution': 1 });

// Hash password before saving
UserSchema.pre('save', async function(next) {
  if (!this.isModified('passwordHash')) return next();
  
  try {
    const salt = await bcrypt.genSalt(12);
    this.passwordHash = await bcrypt.hash(this.passwordHash, salt);
    next();
  } catch (error) {
    next(error as Error);
  }
});

// Compare password method
UserSchema.methods.comparePassword = async function(candidatePassword: string): Promise<boolean> {
  return bcrypt.compare(candidatePassword, this.passwordHash);
};

// Remove sensitive data when converting to JSON
UserSchema.methods.toJSON = function() {
  const obj = this.toObject();
  delete obj.passwordHash;
  return obj;
};

export default mongoose.model<IUser>('User', UserSchema);
