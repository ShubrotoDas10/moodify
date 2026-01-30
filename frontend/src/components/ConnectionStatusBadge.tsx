import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertCircle, CheckCircle2, Loader2, WifiOff } from 'lucide-react';

export type ConnectionStatus = 'checking' | 'connected' | 'error' | 'disconnected';

interface ConnectionStatusBadgeProps {
  status: ConnectionStatus;
  message?: string;
}

const statusConfig = {
  checking: {
    icon: Loader2,
    label: 'Connecting...',
    className: 'bg-muted text-muted-foreground',
    iconClassName: 'animate-spin',
  },
  connected: {
    icon: CheckCircle2,
    label: 'Connected',
    className: 'bg-emotion-happy/20 text-emotion-happy',
    iconClassName: '',
  },
  error: {
    icon: AlertCircle,
    label: 'Error',
    className: 'bg-destructive/20 text-destructive',
    iconClassName: '',
  },
  disconnected: {
    icon: WifiOff,
    label: 'Disconnected',
    className: 'bg-emotion-neutral/20 text-emotion-neutral',
    iconClassName: '',
  },
};

export const ConnectionStatusBadge: React.FC<ConnectionStatusBadgeProps> = ({
  status,
  message,
}) => {
  const config = statusConfig[status];
  const Icon = config.icon;

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={status}
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
        className={`inline-flex items-center gap-1.5 px-2 py-1 rounded-full text-xs ${config.className}`}
      >
        <Icon className={`w-3 h-3 ${config.iconClassName}`} />
        <span>{message || config.label}</span>
      </motion.div>
    </AnimatePresence>
  );
};

export default ConnectionStatusBadge;
