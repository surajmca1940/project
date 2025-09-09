import mongoose, { Document, Schema } from 'mongoose';

export interface IAppointment extends Document {
  studentId: mongoose.Types.ObjectId;
  counselorId: mongoose.Types.ObjectId;
  datetime: Date;
  duration: number; // in minutes
  status: 'scheduled' | 'completed' | 'cancelled' | 'rescheduled' | 'no-show';
  type: 'individual' | 'group' | 'crisis';
  mode: 'in-person' | 'video' | 'phone';
  reason: string;
  notes?: {
    studentNotes?: string;
    counselorNotes?: string; // encrypted
    privateNotes?: string; // encrypted, counselor only
  };
  followUp?: {
    required: boolean;
    scheduledDate?: Date;
    notes?: string;
  };
  feedback?: {
    studentRating?: number;
    studentComments?: string;
    counselorRating?: number;
    effectiveness?: number;
  };
  reminders: {
    sent24h: boolean;
    sent1h: boolean;
    sentNow: boolean;
  };
  createdAt: Date;
  updatedAt: Date;
}

const AppointmentSchema = new Schema<IAppointment>({
  studentId: {
    type: Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  counselorId: {
    type: Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  datetime: {
    type: Date,
    required: true
  },
  duration: {
    type: Number,
    default: 60,
    min: 15,
    max: 120
  },
  status: {
    type: String,
    enum: ['scheduled', 'completed', 'cancelled', 'rescheduled', 'no-show'],
    default: 'scheduled'
  },
  type: {
    type: String,
    enum: ['individual', 'group', 'crisis'],
    default: 'individual'
  },
  mode: {
    type: String,
    enum: ['in-person', 'video', 'phone'],
    default: 'in-person'
  },
  reason: {
    type: String,
    required: true,
    trim: true,
    maxlength: 500
  },
  notes: {
    studentNotes: {
      type: String,
      maxlength: 1000
    },
    counselorNotes: {
      type: String,
      maxlength: 2000
    },
    privateNotes: {
      type: String,
      maxlength: 1000
    }
  },
  followUp: {
    required: {
      type: Boolean,
      default: false
    },
    scheduledDate: {
      type: Date
    },
    notes: {
      type: String,
      maxlength: 500
    }
  },
  feedback: {
    studentRating: {
      type: Number,
      min: 1,
      max: 5
    },
    studentComments: {
      type: String,
      maxlength: 500
    },
    counselorRating: {
      type: Number,
      min: 1,
      max: 5
    },
    effectiveness: {
      type: Number,
      min: 1,
      max: 5
    }
  },
  reminders: {
    sent24h: {
      type: Boolean,
      default: false
    },
    sent1h: {
      type: Boolean,
      default: false
    },
    sentNow: {
      type: Boolean,
      default: false
    }
  }
}, {
  timestamps: true,
  collection: 'appointments'
});

// Indexes for better query performance
AppointmentSchema.index({ studentId: 1, datetime: 1 });
AppointmentSchema.index({ counselorId: 1, datetime: 1 });
AppointmentSchema.index({ datetime: 1 });
AppointmentSchema.index({ status: 1 });
AppointmentSchema.index({ type: 1 });

// Compound indexes
AppointmentSchema.index({ counselorId: 1, status: 1, datetime: 1 });
AppointmentSchema.index({ studentId: 1, status: 1, datetime: 1 });

// Validation: appointment must be in the future
AppointmentSchema.pre('save', function(next) {
  if (this.isNew && this.datetime <= new Date()) {
    return next(new Error('Appointment date must be in the future'));
  }
  next();
});

// Virtual for populating user details
AppointmentSchema.virtual('student', {
  ref: 'User',
  localField: 'studentId',
  foreignField: '_id',
  justOne: true
});

AppointmentSchema.virtual('counselor', {
  ref: 'User',
  localField: 'counselorId',
  foreignField: '_id',
  justOne: true
});

// Ensure virtual fields are serialized
AppointmentSchema.set('toJSON', { virtuals: true });

export default mongoose.model<IAppointment>('Appointment', AppointmentSchema);
