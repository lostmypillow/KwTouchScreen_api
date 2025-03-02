class Countdown {
  constructor(initialTime = 30, onExpire = () => {}, onTick = () => {}) {
    this.countdown = initialTime;
    this.countdownInterval = null;
    this.onExpire = onExpire;
    this.onTick = onTick;
  }

  // Helper function to get the current timestamp
  getTimestamp() {
    return new Date().toISOString();
  }

  // Helper function to log messages with timestamps and origin
  logWithTimestamp(level, message) {
    console[level](`[Countdown.js] [${this.getTimestamp()}] ${message}`);
  }

  start() {
    try {
      if (this.countdownInterval) {
        clearInterval(this.countdownInterval);
        this.logWithTimestamp('log', 'Previous countdown cleared.');
      }

      this.countdownInterval = setInterval(() => {
        if (this.countdown <= 0) {
          this.logWithTimestamp('warn', 'Countdown expired prematurely!');
          clearInterval(this.countdownInterval);
          this.onExpire();
          return;
        }

        this.countdown--;
        this.onTick(this.countdown);

        if (this.countdown <= 0) {
          clearInterval(this.countdownInterval);
          this.onExpire();
          this.logWithTimestamp('log', 'Countdown expired and stopped.');
        }
      }, 1000);
      this.logWithTimestamp('log', `Countdown started with ${this.countdown} seconds.`);
    } catch (error) {
      this.logWithTimestamp('error', `Error starting countdown: ${error}`);
    }
  }

  reset(initialTime = 30) {
    try {
      this.countdown = initialTime;
      this.logWithTimestamp('log', `Countdown reset to ${initialTime} seconds.`);
      this.start();
    } catch (error) {
      this.logWithTimestamp('error', `Error resetting countdown: ${error}`);
    }
  }

  stop() {
    try {
      if (this.countdownInterval) {
        clearInterval(this.countdownInterval);
        this.countdownInterval = null;
        this.logWithTimestamp('log', 'Countdown stopped.');
      }
    } catch (error) {
      this.logWithTimestamp('error', `Error stopping countdown: ${error}`);
    }
  }

  getRemainingTime() {
    try {
      return this.countdown;
    } catch (error) {
      this.logWithTimestamp('error', `Error getting remaining time: ${error}`);
      return null;
    }
  }
}

export default Countdown;
