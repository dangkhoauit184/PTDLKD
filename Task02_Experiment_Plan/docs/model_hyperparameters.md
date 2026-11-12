# Đặc Tả Siêu Tham Số Các Mô Hình Khôi Phục (Latent Demand Recovery)

Nguồn: Đối chiếu giữa Bảng 2 bài báo và `models.py` trong repo baseline.

| Mô hình | Tham số tầng / Ẩn | Tham số đặc thù trong `models.py` | Optimizer & Loss |
| :--- | :--- | :--- | :--- |
| **TimesNet** | `n_layers=2`, `d_model=64`, `d_ffn=32` | `top_k=7`, `n_kernels=5`, `apply_nonstationary_norm=True` | Adam, lr=0.001, MAE loss |
| **ImputeFormer** | `n_layers=2`, `d_proj=64`, `d_ffn=32` | `n_temporal_heads=4`, `d_input_embed=64`, `d_learnable_embed=32` | Adam, lr=0.001, ORT+MIT loss |
| **SAITS** | `n_layers=2`, `d_model=64`, `n_heads=4` | `d_k=16`, `d_v=16`, `diagonal_attention_mask=True` | Adam, lr=0.001, customized MAE |
| **iTransformer** | `n_layers=2`, `d_model=64`, `n_heads=4` | `d_k=16`, `d_v=16`, `d_ffn=32` | Adam, lr=0.001, ORT+MIT loss |
| **GPVAE** | `encoder=(64,64)`, `decoder=(64,64)` | `latent_size=4`, `kernel="cauchy"`, `beta=0.01`, `sigma=1.0`, `length_scale=48.0` | Adam, lr=0.001 |
| **CSDI** | `n_layers=2`, `n_heads=4`, `channels=32`| `n_diffusion_steps=30`, `schedule='linear'`, `beta_start=0.0001`, `beta_end=0.04` | Adam, lr=0.001 |
| **DLinear** | Tuyến tính một lớp | `moving_avg_window_size=17`, `individual=False` | Adam, lr=0.001, ORT+MIT loss |
