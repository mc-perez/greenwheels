type ErrorBannerProps = {
  message: string | null;
  onDismiss?: () => void;
};

export function ErrorBanner({ message, onDismiss }: ErrorBannerProps) {
  if (!message) {
    return null;
  }
  return (
    <div className="error-banner" role="alert">
      <span>{message}</span>
      {onDismiss ? (
        <button type="button" className="btn-link" onClick={onDismiss} aria-label="Dismiss">
          Dismiss
        </button>
      ) : null}
    </div>
  );
}
