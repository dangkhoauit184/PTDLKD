# Task 16 — Kiểm định Thống kê (IS403), Trực quan hóa Ma trận & Đóng gói Cuối kỳ

Thư mục này khép kín toàn bộ quy trình thực nghiệm **Task 1 → Task 16** của đồ án môn **Phân tích Dữ liệu Kinh doanh (`IS403`)** trên bộ dữ liệu bán lẻ đồ tươi sống **FreshRetailNet-50K**:
- Kiểm định giả thuyết thống kê chuẩn **Chương 2 IS403** (*Paired Student's $t$-test*, *Wilcoxon Signed-Rank*, *Tiền kiểm định Levene*, *One-Way ANOVA*, *Hậu kiểm Tukey's HSD*, *Friedman Block Test*, *Two-Way ANOVA* và *Kiểm định tương đương tái lập*).
- Phân tích định lượng trên `4.500.000` dòng lịch sử giải mã cơ chế gây thiên lệch dương ở `DLinear + RevIN` trên nhóm `Low Sale` (`50,43%` chuỗi có $\sigma < 0,30$) đối lập với sự ổn định của `SSA` và kiến trúc SOTA `TFT`.
- Xuất bộ **6 biểu đồ tổng hợp cuối kỳ (`300 DPI`)**, quyển **Báo cáo tổng kết Word (`.docx`)** và **Slide thuyết trình cuối kỳ (`.md` & `.html`)**.

## Cấu trúc thư mục
```text
Task16_Final_Synthesis/
├── README.md
├── run_info.md
├── notebooks/
│   └── 16_final_synthesis.ipynb
├── deliverables/
│   ├── Bao_Cao_Cuoi_Ky_IS403_FreshRetailNet50K.docx
│   ├── Slide_Thuyet_Trinh_IS403_FreshRetailNet50K.md
│   └── Slide_Thuyet_Trinh_IS403_FreshRetailNet50K.html
└── results/
    ├── master_artifacts_index.csv
    ├── table2_recovery_summary.csv
    ├── table3_all_8configs_summary.csv
    ├── recovery_regime_mechanism.csv
    ├── ssa_daily_7days_metrics.csv
    ├── statistical_tests_is403.csv
    ├── run_metadata.json
    ├── full/
    │   └── task16_statistical_synthesis.log
    └── figures/
        ├── 01_stage1_recovery_table2_comparison.png
        ├── 02_table3_wape_matrix_all8_configs.png
        ├── 03_wape_vs_wpe_pareto_tradeoff.png
        ├── 04_is403_anova_and_interaction_plots.png
        ├── 05_paper_replication_fidelity_parity.png
        └── 06_fresh_retail_inventory_strategy_matrix.png
```

## Tài liệu liên quan
- Báo cáo phân tích chi tiết Task 16: [Task16_Report.md](../reports/Task16_Report.md)
- Báo cáo tổng hợp toàn dự án: [Synthesis_Report.md](../reports/Synthesis_Report.md)
- Biên bản chạy & danh mục link Google Drive / SHA-256: [run_info.md](run_info.md)
