import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  Box, Container, Typography, Button, Paper,
  TextField, Divider, Alert, CircularProgress,
} from "@mui/material";
import Navbar from "../components/Navbar";
import { useCart } from "../context/CartContext";
import { useAuth } from "../context/AuthContext";
import api from "../utils/api";

const Checkout = () => {
  const { cart, fetchCart, clearCart } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [address, setAddress] = useState({
    street: "",
    city: "",
    state: "",
    pincode: "",
  });
  const [addressErrors, setAddressErrors] = useState({});

  useEffect(() => {
    if (!user) {
      navigate("/login");
      return;
    }
    fetchCart();
  }, [user]);

  // ── Validate Address ───────────────────────────────
  const validateAddress = () => {
    const errors = {};
    if (!address.street.trim()) errors.street = "Street is required";
    if (!address.city.trim()) errors.city = "City is required";
    if (!address.state.trim()) errors.state = "State is required";
    if (!address.pincode.trim()) errors.pincode = "Pincode is required";
    else if (!/^\d{6}$/.test(address.pincode))
      errors.pincode = "Enter valid 6 digit pincode";
    return errors;
  };

  // ── Calculate Total ────────────────────────────────
  const total = cart.reduce((sum, item) => {
    return sum + item.product.price * item.quantity;
  }, 0);

  // ── Handle Payment ─────────────────────────────────
  const handlePayment = async () => {
    setError("");
    setSuccess("");

    const errors = validateAddress();
    if (Object.keys(errors).length > 0) {
      setAddressErrors(errors);
      return;
    }

    if (cart.length === 0) {
      setError("Your cart is empty");
      return;
    }

    setLoading(true);

    try {
      await api.post("/orders/dummy-payment", {
        shippingAddress: address,
      });

      await clearCart();
      setSuccess("Payment done. Order placed successfully.");
      setTimeout(() => navigate("/orders"), 1000);
    } catch (err) {
      setError(
        err.response?.data?.message ||
        err.response?.data?.detail ||
        "Payment failed. Try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ minHeight: "100vh", bgcolor: "grey.50" }}>
      <Navbar />

      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Typography variant="h5" fontWeight={800} mb={3}>
          Checkout
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}
        {success && (
          <Alert severity="success" sx={{ mb: 3 }}>
            {success}
          </Alert>
        )}

        <Box sx={{
          display: "flex", gap: 3,
          flexDirection: { xs: "column", md: "row" }
        }}>

          {/* Shipping Address */}
          <Box sx={{ flex: 1 }}>
            <Paper
              elevation={0}
              sx={{
                p: 3, borderRadius: 3,
                border: "1px solid", borderColor: "grey.200",
              }}
            >
              <Typography variant="h6" fontWeight={700} mb={2}>
                Shipping Address
              </Typography>

              <TextField
                fullWidth label="Street Address"
                value={address.street}
                onChange={(e) => {
                  setAddress({ ...address, street: e.target.value });
                  setAddressErrors({ ...addressErrors, street: "" });
                }}
                error={!!addressErrors.street}
                helperText={addressErrors.street}
                margin="normal"
              />

              <TextField
                fullWidth label="City"
                value={address.city}
                onChange={(e) => {
                  setAddress({ ...address, city: e.target.value });
                  setAddressErrors({ ...addressErrors, city: "" });
                }}
                error={!!addressErrors.city}
                helperText={addressErrors.city}
                margin="normal"
              />

              <TextField
                fullWidth label="State"
                value={address.state}
                onChange={(e) => {
                  setAddress({ ...address, state: e.target.value });
                  setAddressErrors({ ...addressErrors, state: "" });
                }}
                error={!!addressErrors.state}
                helperText={addressErrors.state}
                margin="normal"
              />

              <TextField
                fullWidth label="Pincode"
                value={address.pincode}
                onChange={(e) => {
                  setAddress({ ...address, pincode: e.target.value });
                  setAddressErrors({ ...addressErrors, pincode: "" });
                }}
                error={!!addressErrors.pincode}
                helperText={addressErrors.pincode}
                margin="normal"
                inputProps={{ maxLength: 6 }}
              />
            </Paper>
          </Box>

          {/* Order Summary */}
          <Box sx={{ width: { xs: "100%", md: 320 } }}>
            <Paper
              elevation={0}
              sx={{
                p: 3, borderRadius: 3,
                border: "1px solid", borderColor: "grey.200",
                position: { md: "sticky" },
                top: { md: 80 },
              }}
            >
              <Typography variant="h6" fontWeight={700} mb={2}>
                Order Summary
              </Typography>

              <Divider sx={{ mb: 2 }} />

              {cart.map((item) => (
                <Box
                  key={item.product._id}
                  sx={{ display: "flex", justifyContent: "space-between", mb: 1 }}
                >
                  <Typography
                    variant="body2" color="text.secondary"
                    sx={{
                      maxWidth: 180,
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                      whiteSpace: "nowrap",
                    }}
                  >
                    {item.product.name} x{item.quantity}
                  </Typography>
                  <Typography variant="body2" fontWeight={600}>
                    ₹{(item.product.price * item.quantity).toLocaleString()}
                  </Typography>
                </Box>
              ))}

              <Divider sx={{ my: 2 }} />

              {/* Total */}
              <Box sx={{ display: "flex", justifyContent: "space-between", mb: 3 }}>
                <Typography variant="h6" fontWeight={800}>Total</Typography>
                <Typography variant="h6" fontWeight={800} color="primary">
                  ₹{total.toLocaleString()}
                </Typography>
              </Box>

              {/* Pay Button */}
              <Button
                fullWidth variant="contained" size="large"
                onClick={handlePayment}
                disabled={loading || cart.length === 0}
                sx={{ borderRadius: 2, py: 1.5, fontWeight: 700, mb: 2 }}
              >
                {loading
                  ? <CircularProgress size={24} color="inherit" />
                  : `Pay ₹${total.toLocaleString()}`
                }
              </Button>

              <Button
                fullWidth variant="outlined" size="large"
                onClick={() => navigate("/cart")}
                sx={{ borderRadius: 2, py: 1.5, fontWeight: 700 }}
              >
                Back to Cart
              </Button>
            </Paper>
          </Box>
        </Box>
      </Container>
    </Box>
  );
};

export default Checkout;
