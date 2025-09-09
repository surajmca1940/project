import mongoose, { Document, Schema } from 'mongoose';

export interface IChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string; // encrypted
  timestamp: Date;
  metadata?: {
    sentiment?: 'positive' | 'negative' | 'neutral' | 'concerning';
    riskLevel?: 'low' | 'medium' | 'high' | 'critical';
    topics?: string[];
    confidence?: number;
  };
}

export interface IChatSession extends Document {
  userId: mongoose.Types.ObjectId;
  sessionId: string;
  messages: IChatMessage[];
  summary?: {
    sentiment: 'positive' | 'negative' | 'neutral' | 'concerning';
    riskLevel: 'low' | 'medium' | 'high' | 'critical';
    mainTopics: string[];
    recommendations?: string[];
    needsHumanIntervention: boolean;
  };
  analytics: {
    messageCount: number;
    avgSentiment: number;
    sessionDuration: number; // in minutes
    engagementScore: number; // 1-10
  };
  status: 'active' | 'completed' | 'escalated' | 'abandoned';
  escalation?: {
    triggered: boolean;
    reason: string;
    timestamp: Date;
    counselorNotified: boolean;
    adminNotified: boolean;
  };
  feedback?: {
    rating: number; // 1-5
    helpful: boolean;
    comments?: string;
  };
  createdAt: Date;
  updatedAt: Date;
}

const ChatMessageSchema = new Schema<IChatMessage>({
  role: {
    type: String,
    enum: ['user', 'assistant', 'system'],
    required: true
  },
  content: {
    type: String,
    required: true
  },
  timestamp: {
    type: Date,
    default: Date.now
  },
  metadata: {
    sentiment: {
      type: String,
      enum: ['positive', 'negative', 'neutral', 'concerning']
    },
    riskLevel: {
      type: String,
      enum: ['low', 'medium', 'high', 'critical']
    },
    topics: [{
      type: String,
      trim: true
    }],
    confidence: {
      type: Number,
      min: 0,
      max: 1
    }
  }
}, { _id: false });

const ChatSessionSchema = new Schema<IChatSession>({
  userId: {
    type: Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  sessionId: {
    type: String,
    required: true,
    unique: true,
    index: true
  },
  messages: [ChatMessageSchema],
  summary: {
    sentiment: {
      type: String,
      enum: ['positive', 'negative', 'neutral', 'concerning']
    },
    riskLevel: {
      type: String,
      enum: ['low', 'medium', 'high', 'critical'],
      default: 'low'
    },
    mainTopics: [{
      type: String,
      trim: true
    }],
    recommendations: [{
      type: String,
      trim: true
    }],
    needsHumanIntervention: {
      type: Boolean,
      default: false
    }
  },
  analytics: {
    messageCount: {
      type: Number,
      default: 0
    },
    avgSentiment: {
      type: Number,
      min: -1,
      max: 1,
      default: 0
    },
    sessionDuration: {
      type: Number,
      default: 0
    },
    engagementScore: {
      type: Number,
      min: 1,
      max: 10,
      default: 5
    }
  },
  status: {
    type: String,
    enum: ['active', 'completed', 'escalated', 'abandoned'],
    default: 'active'
  },
  escalation: {
    triggered: {
      type: Boolean,
      default: false
    },
    reason: {
      type: String,
      trim: true
    },
    timestamp: {
      type: Date
    },
    counselorNotified: {
      type: Boolean,
      default: false
    },
    adminNotified: {
      type: Boolean,
      default: false
    }
  },
  feedback: {
    rating: {
      type: Number,
      min: 1,
      max: 5
    },
    helpful: {
      type: Boolean
    },
    comments: {
      type: String,
      maxlength: 500
    }
  }
}, {
  timestamps: true,
  collection: 'chat_sessions'
});

// Indexes for better query performance
ChatSessionSchema.index({ userId: 1, createdAt: -1 });
ChatSessionSchema.index({ sessionId: 1 });
ChatSessionSchema.index({ status: 1 });
ChatSessionSchema.index({ 'summary.riskLevel': 1 });
ChatSessionSchema.index({ 'escalation.triggered': 1 });
ChatSessionSchema.index({ createdAt: -1 });

// Compound indexes
ChatSessionSchema.index({ userId: 1, status: 1 });
ChatSessionSchema.index({ 'summary.riskLevel': 1, 'escalation.triggered': 1 });

// Pre-save middleware to update analytics
ChatSessionSchema.pre('save', function(next) {
  if (this.isModified('messages')) {
    this.analytics.messageCount = this.messages.length;
    
    // Calculate average sentiment
    const sentimentValues = this.messages
      .filter(msg => msg.metadata?.sentiment)
      .map(msg => {
        switch (msg.metadata!.sentiment) {
          case 'positive': return 1;
          case 'neutral': return 0;
          case 'negative': return -0.5;
          case 'concerning': return -1;
          default: return 0;
        }
      });
    
    if (sentimentValues.length > 0) {
      this.analytics.avgSentiment = sentimentValues.reduce((a, b) => a + b, 0) / sentimentValues.length;
    }
    
    // Update session duration
    if (this.messages.length > 1) {
      const firstMessage = this.messages[0];
      const lastMessage = this.messages[this.messages.length - 1];
      this.analytics.sessionDuration = Math.round(
        (lastMessage.timestamp.getTime() - firstMessage.timestamp.getTime()) / (1000 * 60)
      );
    }
  }
  next();
});

// Virtual for populating user details
ChatSessionSchema.virtual('user', {
  ref: 'User',
  localField: 'userId',
  foreignField: '_id',
  justOne: true
});

// Ensure virtual fields are serialized
ChatSessionSchema.set('toJSON', { virtuals: true });

export default mongoose.model<IChatSession>('ChatSession', ChatSessionSchema);
