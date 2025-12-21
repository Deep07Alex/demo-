/* ---------- helpers ---------- */
const $ = (q) => document.querySelector(q);
const $$ = (q) => document.querySelectorAll(q);

/* ---------- dom refs ---------- */
const sendOtpBtn = $("#sendOtpBtn");
const phoneInput = $("#phone");
const otpModal = $("#otpModal");
const maskedPhone = $("#maskedPhone");
const closeOtpBtn = $("#closeOtp");
const resendOtpBtn = $("#resendOtp");
const verifyOtpBtn = $("#verifyOtpBtn");
const otpDigits = $$(".otp-digit");
const otpHint = $("#otpHint");
const otpTimer = $("#otpTimer");
const addressSec = $("#addressSection");
const payBtn = $("#payBtn"); // <-- ADD THIS

/* ---------- state ---------- */
let currentVerificationId = null;
let timerInterval = null;

/* ---------- utility ---------- */
const formatPhone = (p) => {
  return p.length >= 10 ? `${p.slice(0, 3)}****${p.slice(-3)}` : p;
};

const startTimer = () => {
  let s = 60;
  clearInterval(timerInterval);
  otpTimer.textContent = "01:00";
  timerInterval = setInterval(() => {
    s--;
    const mins = Math.floor(s / 60);
    const secs = s % 60;
    otpTimer.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    if (s === 0) {
      clearInterval(timerInterval);
      resendOtpBtn.disabled = false;
      resendOtpBtn.classList.remove("opacity-50");
    }
  }, 1000);
};

/* ---------- send otp ---------- */
if (sendOtpBtn) {
  sendOtpBtn.addEventListener("click", async () => {
    const phone = phoneInput.value.trim();
    const deliveryMethod = document.querySelector('input[name="deliveryMethod"]:checked')?.value || 'sms';
    
    if (phone.length < 10) {
      alert("Enter a valid 10-digit number");
      return;
    }
    
    sendOtpBtn.disabled = true;
    sendOtpBtn.textContent = "Sending...";
    
    try {
      const response = await fetch('/api/send-otp/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
          phone: phone,
          delivery_method: deliveryMethod
        })
      });
      
      const data = await response.json();
      
      if (data.success) {
        currentVerificationId = data.verification_id;
        maskedPhone.textContent = formatPhone(phone);
        otpModal.classList.remove("hidden");
        otpHint.textContent = `OTP sent via ${deliveryMethod}`;
        startTimer();
        otpDigits[0].focus();
      } else {
        alert(data.error || "Failed to send OTP");
      }
    } catch (error) {
      console.error('Send OTP error:', error);
      alert("An error occurred. Please try again.");
    } finally {
      sendOtpBtn.disabled = false;
      sendOtpBtn.textContent = "Send OTP";
    }
  });
}

if (closeOtpBtn) {
  closeOtpBtn.addEventListener("click", () => {
    otpModal.classList.add("hidden");
    clearInterval(timerInterval);
  });
}

/* ---------- otp digit auto-tab ---------- */
otpDigits.forEach((inp, idx) => {
  inp.addEventListener("input", (e) => {
    if (e.target.value && idx < otpDigits.length - 1) {
      otpDigits[idx + 1].focus();
    }
  });
  inp.addEventListener("keydown", (e) => {
    if (e.key === "Backspace" && !e.target.value && idx > 0) {
      otpDigits[idx - 1].focus();
    }
  });
});

/* ---------- verify otp ---------- */
if (verifyOtpBtn) {
  verifyOtpBtn.addEventListener("click", async () => {
    const enteredOtp = Array.from(otpDigits).map(d => d.value).join("");
    
    if (enteredOtp.length !== 6) {
      otpHint.textContent = "Please enter complete 6-digit OTP";
      return;
    }
    
    verifyOtpBtn.disabled = true;
    verifyOtpBtn.textContent = "Verifying...";
    
    try {
      const response = await fetch('/api/verify-otp/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
          verification_id: currentVerificationId,
          otp: enteredOtp
        })
      });
      
      const data = await response.json();
      
      if (data.success) {
        clearInterval(timerInterval);
        otpModal.classList.add("hidden");
        addressSec.classList.remove("opacity-50", "pointer-events-none");
        addressSec.setAttribute("aria-hidden", "false");
        otpHint.textContent = "Verification successful!";
      } else {
        otpHint.textContent = data.error || "Invalid OTP";
        otpDigits.forEach(d => d.value = "");
        otpDigits[0].focus();
      }
    } catch (error) {
      console.error('Verify OTP error:', error);
      otpHint.textContent = "An error occurred. Please try again.";
    } finally {
      verifyOtpBtn.disabled = false;
      verifyOtpBtn.textContent = "Verify";
    }
  });
}

/* ---------- resend otp ---------- */
if (resendOtpBtn) {
  resendOtpBtn.addEventListener("click", async () => {
    resendOtpBtn.disabled = true;
    resendOtpBtn.classList.add("opacity-50");
    
    try {
      const response = await fetch('/api/resend-otp/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
          verification_id: currentVerificationId
        })
      });
      
      const data = await response.json();
      
      if (data.success) {
        otpDigits.forEach(d => d.value = "");
        otpDigits[0].focus();
        startTimer();
        otpHint.textContent = "OTP resent successfully";
      } else {
        otpHint.textContent = data.error || "Failed to resend OTP";
      }
    } catch (error) {
      console.error('Resend OTP error:', error);
      otpHint.textContent = "An error occurred. Please try again.";
    }
  });
}

/* ---------- payment method switch (FIXED) ---------- */
// Only run if payment method options exist on the page
const payOptions = $$(".pay-option");
if (payOptions.length > 0) {
  payOptions.forEach((btn) => {
    btn.addEventListener("click", () => {
      payOptions.forEach((b) =>
        b.classList.remove("bg-[#e20074]", "text-white")
      );
      btn.classList.add("bg-[#e20074]", "text-white");
      const method = btn.dataset.pay;
      const cardForm = $("#cardForm");
      const upiForm = $("#upiForm");
      const netForm = $("#netForm");
      
      if (cardForm) cardForm.classList.toggle("hidden", method !== "card");
      if (upiForm) upiForm.classList.toggle("hidden", method !== "upi");
      if (netForm) netForm.classList.toggle("hidden", method !== "netbank");
    });
  });
}

/* ---------- card number spacing (FIXED) ---------- */
const cardNumberEl = $("#cardNumber");
if (cardNumberEl) {
  cardNumberEl.addEventListener("input", (e) => {
    e.target.value = e.target.value
      .replace(/\s+/g, "")
      .replace(/(.{4})/g, "$1 ")
      .trim();
  });
}

/* ---------- expiry format (FIXED) ---------- */
const cardExpEl = $("#cardExp");
if (cardExpEl) {
  cardExpEl.addEventListener("input", (e) => {
    const val = e.target.value.replace(/\D/g, "");
    if (val.length >= 2)
      e.target.value = `${val.slice(0, 2)}/${val.slice(2, 4)}`;
    else e.target.value = val;
  });
}

/* ---------- process payment (FIXED SELECTOR) ---------- */
if (payBtn) {
  payBtn.addEventListener("click", async () => {
    console.log("Pay button clicked!");
    
    // FIX: Find active payment method without using problematic class selector
    const activePayOption = document.querySelector('.pay-option.bg-\\[\\#e20074\\]'); // Escaped version
    const paymentMethod = activePayOption ? activePayOption.dataset.pay : 'card';
    
    const orderData = {
      fullname: $("#fullname")?.value || '',
      email: $("#email")?.value || '',
      address: $("#addr")?.value || '',
      city: $("#city")?.value || '',
      state: $("#state")?.value || '',
      pin: $("#pin")?.value || '',
      delivery: $("#delivery")?.value || '',
      payment_method: paymentMethod,
    };
    
    // Validate
    if (!orderData.fullname || !orderData.email || !orderData.address) {
      alert("Please fill all required fields");
      return;
    }
    
    // Verify phone was verified
    if (!currentVerificationId) {
      alert("Please verify your phone number first");
      return;
    }
    
    payBtn.disabled = true;
    payBtn.textContent = "Processing...";
    
    try {
      const response = await fetch('/api/initiate-payment/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify(orderData)
      });
      
      const data = await response.json();
      console.log("Payment response:", data);
      
      if (data.success) {
        // Create and submit PayU form
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = data.payu_url;
        form.style.display = 'none';
        
        Object.entries(data.payu_params).forEach(([key, value]) => {
          const input = document.createElement('input');
          input.type = 'hidden';
          input.name = key;
          input.value = value;
          form.appendChild(input);
        });
        
        document.body.appendChild(form);
        form.submit();
        
      } else {
        alert(data.error || "Failed to initiate payment");
        payBtn.disabled = false;
        payBtn.textContent = `Pay ₹${payBtn.dataset.total}`;
      }
    } catch (error) {
      console.error('Payment error:', error);
      alert("An error occurred. Please try again.");
      payBtn.disabled = false;
      payBtn.textContent = `Pay ₹${payBtn.dataset.total}`;
    }
  });
}

/* ---------- utility function for CSRF token ---------- */
function getCSRFToken() {
  const token = document.cookie.match(/csrftoken=([\w-]+)/)?.[1] || '';
  console.log("CSRF Token:", token); // Debug log
  return token;
}