# Used Computer System Research for Local LLMs
## For: Troy - Budget ~$1,000-$2,000 CAD - GTA/Ontario Area

---

## PART 1: Hardware Requirements for Local LLMs (Qwen & Chinese Models)

### Understanding VRAM Requirements
VRAM is the **single most important factor** for running local LLMs. Here's the breakdown:

| Model Size | Q4 Quantization VRAM | Q8 Quantization VRAM | FP16 VRAM |
|------------|---------------------|---------------------|-----------|
| 7B-8B | 4-6 GB | 8 GB | 16 GB |
| 13B-14B | 8-10 GB | 16 GB | 32 GB |
| 30B-34B | 16-20 GB | 32 GB | 64 GB |
| 70B-72B | 35-40 GB | 70 GB | 140 GB |

**Formula:** VRAM (GB) ≈ Parameters (B) × 0.5 for Q4 quantization

### Specific Qwen Model Requirements

**Qwen2.5 Series:**
- 7B: 6GB VRAM (GPU) or 4GB RAM (CPU)
- 14B: 10GB VRAM recommended
- 32B: 20GB VRAM (Q4 quantization)
- 72B: 40GB+ VRAM or dual GPU setup

**Qwen3 Series (newest):**
- 0.6B-1.7B: 8GB RAM minimum
- 4B-8B: 16GB RAM minimum, 32GB recommended
- 14B-32B: 32GB minimum, 64GB preferred
- MoE models (30B-A3B, 235B-A22B): 64GB+ RAM

### System RAM Requirements
- **Minimum for 7B-13B:** 32GB RAM
- **Recommended for 32B models:** 64GB RAM  
- **For 70B models:** 64-128GB RAM (or dual GPU)

### CPU Requirements
- Modern multi-core CPU (Intel i7 8th gen+ or AMD Ryzen 5 3rd gen+)
- 6-8 cores ideal
- 3.6GHz+ clock speed
- AVX2 instruction set support (required for llama.cpp CPU inference)

### Storage Requirements
- **7B model:** 4-8GB
- **13B model:** 8-15GB
- **70B model:** 35-70GB
- **Recommendation:** 1-2TB NVMe SSD (fast loading essential)

---

## PART 2: What to Look for in Used Systems

### GPU Priority List (Best Value for LLMs)

| GPU | VRAM | Used Price (CAD) | LLM Capability |
|-----|------|------------------|----------------|
| RTX 3060 12GB | 12GB | $250-350 | 7B-13B models, tight on 30B |
| RTX 3070 8GB | 8GB | $250-350 | 7B models only |
| RTX 3080 10GB | 10GB | $400-520 | 7B-13B models |
| RTX 3080 Ti 12GB | 12GB | $500-600 | 7B-13B models |
| **RTX 3090 24GB** | **24GB** | **$800-950** | **7B-32B models, tight 70B** |
| RTX 4070 Ti Super | 16GB | $800-1000 | Up to 32B comfortably |
| RX 7900 XTX | 24GB | $900-1000 | 7B-32B models |

**🏆 BEST VALUE: RTX 3090 24GB** - This is the "value king" for local LLMs. The 24GB VRAM allows running 32B models comfortably and 70B models with some optimization.

### CPU Priority List
- **AMD Ryzen 7/9 3000-series or newer** (3700X, 5800X, 5900X, 7600X)
- **Intel i7/i9 10th gen or newer** (10700K, 11700K, 12700K)
- Avoid older Xeon workstations unless they come with a powerful GPU

### RAM Configuration
- **Minimum:** 32GB DDR4/DDR5
- **Sweet spot:** 64GB DDR4-3200 or DDR5-5600
- **DDR5 advantage:** 20-30% faster for CPU inference (but GPU inference is what matters most)

### Form Factors to Consider

**Gaming PCs (Recommended)**
- ✅ Modern CPUs (AMD Ryzen, Intel Core i7/i9)
- ✅ Consumer GPUs with good CUDA support
- ✅ Easy to upgrade
- ✅ Good value on used market
- ⚠️ May need RAM upgrade

**Workstations (Dell Precision, HP Z, Lenovo ThinkStation)**
- ✅ ECC RAM support
- ✅ Built for 24/7 operation
- ✅ Often have high core count CPUs
- ⚠️ Older Xeons may bottleneck GPU
- ⚠️ Often come with professional GPUs (Quadro) that need replacement
- ⚠️ Power supply limitations for high-end GPUs

**What to Avoid**
- Systems with only 8GB VRAM GPUs (limiting)
- Very old CPUs (pre-2018)
- Laptops (thermal throttling, non-upgradeable)

---

## PART 3: Current Market Listings (GTA Area)

Based on search results from Kijiji and Facebook Marketplace Toronto/GTA:

### 🔥 OPTION 1: High-End - RTX 3090 Based System

**Expected Configuration:**
- GPU: RTX 3090 24GB (~$850 used)
- CPU: Ryzen 7 3700X/5800X or Intel i7 10700K/11700K
- RAM: 32-64GB DDR4
- Storage: 1TB NVMe SSD
- **Estimated Total: $1,500-2,000**

**Current Market References:**
- RTX 3090 cards alone: $850-950 on Kijiji GTA
- Alienware R10/R12 with RTX 3090: ~$1,500-1,800
- Full custom builds with RTX 3090: $1,800-2,200

**Search URLs to Monitor:**
- https://www.kijiji.ca/b-gta-greater-toronto-area/rtx-3090/k0l1700272
- https://www.facebook.com/marketplace/toronto/desktop-computers/

**Pros:**
- 24GB VRAM handles 32B models perfectly, 70B with Q4
- Best price/performance for LLMs
- Can run Qwen2.5-32B and Qwen3-32B locally

**Cons:**
- Higher power consumption (350W)
- Card may have been mined on (check carefully)
- At the top of budget

---

### 💰 OPTION 2: Mid-Range - RTX 3080/4070 Based System

**Example Listing Found:**
- Gaming PC with RTX 3080, Ryzen 5 7600X, 32GB DDR5, 1TB NVMe
- Price range: $1,200-1,500

**Configuration:**
- GPU: RTX 3080 10GB or RTX 4070 12GB
- CPU: Ryzen 5 7600X / Ryzen 7 3700X / i7-10700
- RAM: 32GB DDR4/DDR5
- Storage: 1TB NVMe

**Search URLs:**
- https://www.kijiji.ca/b-desktop-computers/gta-greater-toronto-area/used-gaming-pc/k0c772l1700272

**Pros:**
- Good for 7B-13B models
- More budget-friendly
- Modern DDR5 platform (if 7000-series Ryzen)

**Cons:**
- 10-12GB VRAM limits to 13B models (Qwen2.5-14B borderline)
- Cannot run 32B models comfortably

---

### 🎯 OPTION 3: Budget Sweet Spot - RTX 3060 12GB System

**Configuration:**
- GPU: RTX 3060 12GB (the 12GB is key!)
- CPU: Ryzen 5 3600/5600 or i7-9700/10700
- RAM: 32GB DDR4
- Storage: 512GB-1TB SSD
- **Estimated: $800-1,100**

**Search Terms for Kijiji/Facebook:**
- "RTX 3060 12GB gaming PC"
- "Used gaming PC 32GB RAM"

**Pros:**
- Under $1,000 target
- 12GB VRAM handles 13B models
- Very cost-effective

**Cons:**
- Limited to 7B-13B models
- Slower inference than higher-end cards

---

### 🏢 OPTION 4: Workstation Route

**Dell Precision / HP Z / Lenovo ThinkStation**

**Examples Found:**
- Dell Precision T7920: Dual Xeon, 32-64GB RAM, $1,000-1,500
- HP Z6 G4: Xeon Gold, 32GB RAM, ~$1,200

**What to Look For:**
- Dell Precision T5820/T7820/T7920
- HP Z4/Z6/Z8 G4
- Lenovo ThinkStation P520/P720/P920

**Critical Consideration:**
Workstations often come with Quadro GPUs that are NOT good for LLMs. You'd need to:
1. Buy the workstation (~$800-1,200)
2. Add a consumer GPU separately ($300-900)
3. Check power supply can handle the GPU

**Pros:**
- Built for 24/7 operation
- Can add lots of RAM
- Professional build quality

**Cons:**
- Older Xeon CPUs may bottleneck
- Need GPU upgrade
- More complex setup

---

## PART 4: Final Recommendations

### 🏆 TOP RECOMMENDATION: RTX 3090 Based System (~$1,500-1,800)

**Why:** The 24GB VRAM is the sweet spot for running 32B models like Qwen2.5-32B and Qwen3-32B, which offer excellent performance for complex tasks.

**Target Specs:**
- RTX 3090 24GB GPU
- Ryzen 7 5800X / 3700X or Intel i7-11700K
- 32GB DDR4 (upgradeable to 64GB)
- 1TB NVMe SSD
- 750W+ PSU

**Where to Find:**
- Search Kijiji GTA for "RTX 3090 gaming PC"
- Check Facebook Marketplace Toronto for complete builds
- Look for Alienware R10/R12 prebuilts

---

### 💰 BUDGET RECOMMENDATION: RTX 3060 12GB System (~$800-1,000)

**Why:** The 12GB VRAM can handle 13B models which are still very capable for most tasks.

**Target Specs:**
- RTX 3060 12GB (not the 8GB version!)
- Ryzen 5 5600 or Intel i7-10700
- 32GB DDR4
- 512GB-1TB SSD

**Models You Can Run:**
- Qwen2.5-7B/14B (14B might be tight)
- Qwen3-8B comfortably
- All 7B parameter models excellently

---

### 🔄 UPGRADE PATH STRATEGY

If buying under budget now with plans to upgrade:

1. **Buy a system with good CPU, RAM, PSU but budget GPU**
   - Ryzen 7 5800X system with RTX 3060: ~$1,000
   - Later upgrade to RTX 3090/4090

2. **Or buy a workstation + separate GPU**
   - Dell Precision T7920: ~$800
   - Add RTX 3090: ~$850
   - Total: ~$1,650

---

## PART 5: Action Items for Troy

### Immediate Search Strategy

1. **Set up Kijiji alerts for:**
   - "RTX 3090 gaming PC" in GTA
   - "RTX 3080 gaming PC" in GTA
   - "Alienware RTX 3090"

2. **Check Facebook Marketplace:**
   - Toronto desktop computers category
   - Search "gaming PC RTX 30"

3. **Key Questions to Ask Sellers:**
   - Was the GPU used for mining? (Check VRAM health)
   - What's the power supply wattage?
   - How much RAM? (32GB minimum, 64GB ideal)
   - Any warranty remaining?

4. **Verify Before Buying:**
   - Test the GPU with a stress test
   - Check GPU-Z for VRAM temperature history
   - Ensure PSU is 750W+ for RTX 3090

### Software Setup Notes

Once you have the hardware, install:
- **Ollama** - Easiest way to run local LLMs
- **LM Studio** - Good GUI for model management
- **llama.cpp** - Most efficient inference engine

Recommended Qwen models to start:
- Qwen2.5-7B-Instruct (easy entry)
- Qwen2.5-14B-Instruct (good performance)
- Qwen2.5-32B-Instruct (if you have 24GB VRAM)

---

## Summary

| Budget | Recommended GPU | Models You Can Run | Expected Price |
|--------|-----------------|-------------------|----------------|
| $800-1,000 | RTX 3060 12GB | 7B-13B | $800-1,100 |
| $1,000-1,500 | RTX 3080 10GB | 7B-13B | $1,200-1,500 |
| $1,500-2,000 | **RTX 3090 24GB** | **7B-32B** | **$1,500-1,800** |

**Bottom Line:** For your budget and goals, a used system with an RTX 3090 24GB offers the best value and will handle Qwen 32B models comfortably. Look for complete gaming PC builds on Kijiji GTA and Facebook Marketplace Toronto in the $1,500-1,800 range.
