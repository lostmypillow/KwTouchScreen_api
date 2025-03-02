class Countdown {
  constructor(initialTime = 30, onExpire = () => {}, onTick = () => {}) {
    this.countdown = initialTime;
    this.countdownInterval = null;
    this.onExpire = onExpire;
    this.onTick = onTick;
  }

  start() {
    if (this.countdownInterval) {
      clearInterval(this.countdownInterval);
    }

    this.countdownInterval = setInterval(() => {
      this.countdown--;
      this.onTick(this.countdown);

      if (this.countdown <= 0) {
        clearInterval(this.countdownInterval);
        this.onExpire();
      }
    }, 1000);
  }

  reset(initialTime = 30) {
    this.countdown = initialTime;
    this.start();
  }

  stop() {
    if (this.countdownInterval) {
      clearInterval(this.countdownInterval);
    }
  }

  getRemainingTime() {
    return this.countdown;
  }
}

export default Countdown;
