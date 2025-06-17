// Main JavaScript file for the data analysis platform

let analysisData = null

document.addEventListener("DOMContentLoaded", () => {
  // Initialize tooltips
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map((tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl))

  // File upload preview
  const fileInput = document.getElementById("file")
  if (fileInput) {
    fileInput.addEventListener("change", handleFileSelect)
  }

  // Form validation
  const forms = document.querySelectorAll("form")
  forms.forEach((form) => {
    form.addEventListener("submit", handleFormSubmit)
  })

  // Auto-resize textareas
  const textareas = document.querySelectorAll("textarea")
  textareas.forEach((textarea) => {
    textarea.addEventListener("input", autoResize)
  })

  // Initialize theme
  initializeTheme()
})

function handleFileSelect(event) {
  const file = event.target.files[0]
  const preview = document.getElementById("filePreview")

  if (!file) {
    preview.innerHTML = '<p class="text-muted mb-0">Dosya seçildikten sonra önizleme burada görünecek</p>'
    return
  }

  // File info
  const fileInfo = `
        <div class="row">
            <div class="col-md-6">
                <strong>Dosya Adı:</strong> ${file.name}<br>
                <strong>Boyut:</strong> ${formatFileSize(file.size)}<br>
                <strong>Tip:</strong> ${file.type || "Bilinmiyor"}
            </div>
            <div class="col-md-6">
                <strong>Son Değişiklik:</strong> ${new Date(file.lastModified).toLocaleString("tr-TR")}
            </div>
        </div>
    `

  preview.innerHTML = fileInfo

  // Try to preview file content for text files
  if (file.type === "text/csv" || file.name.endsWith(".csv")) {
    previewCSVFile(file, preview)
  } else if (file.type === "application/json" || file.name.endsWith(".json")) {
    previewJSONFile(file, preview)
  }
}

function previewCSVFile(file, preview) {
  const reader = new FileReader()
  reader.onload = (e) => {
    const text = e.target.result
    const lines = text.split("\n").slice(0, 5) // First 5 lines
    const previewText = lines.join("\n")

    preview.innerHTML += `
            <hr>
            <h6>Dosya Önizleme (İlk 5 satır):</h6>
            <pre class="bg-light p-2 rounded" style="max-height: 150px; overflow-y: auto;"><code>${previewText}</code></pre>
        `
  }
  reader.readAsText(file)
}

function previewJSONFile(file, preview) {
  const reader = new FileReader()
  reader.onload = (e) => {
    try {
      const json = JSON.parse(e.target.result)
      const previewText = JSON.stringify(json, null, 2).substring(0, 500) + "..."

      preview.innerHTML += `
                <hr>
                <h6>JSON Önizleme:</h6>
                <pre class="bg-light p-2 rounded" style="max-height: 150px; overflow-y: auto;"><code>${previewText}</code></pre>
            `
    } catch (error) {
      preview.innerHTML += `
                <hr>
                <div class="alert alert-warning">JSON dosyası önizlenemiyor: Geçersiz format</div>
            `
    }
  }
  reader.readAsText(file)
}

function formatFileSize(bytes) {
  if (bytes === 0) return "0 Bytes"
  const k = 1024
  const sizes = ["Bytes", "KB", "MB", "GB"]
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Number.parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i]
}

function handleFormSubmit(event) {
  const form = event.target
  const submitBtn = form.querySelector('button[type="submit"]')

  if (submitBtn) {
    // Show loading state
    const originalText = submitBtn.innerHTML
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>İşleniyor...'
    submitBtn.disabled = true

    // Re-enable button after 30 seconds (fallback)
    setTimeout(() => {
      submitBtn.innerHTML = originalText
      submitBtn.disabled = false
    }, 30000)
  }
}

function autoResize(event) {
  const textarea = event.target
  textarea.style.height = "auto"
  textarea.style.height = textarea.scrollHeight + "px"
}

// Chart loading function with error handling
function loadChart(chartType) {
  const container = document.getElementById("chartContainer")
  const buttons = document.querySelectorAll(".btn-group .btn")

  // Update button states
  buttons.forEach((btn) => btn.classList.remove("active"))
  event.target.classList.add("active")

  // Show loading
  container.innerHTML = `
        <div class="text-center py-5">
            <i class="fas fa-spinner fa-spin fa-3x mb-3"></i>
            <p class="text-muted">Grafik oluşturuluyor...</p>
        </div>
    `

  // Check if we have analysis data
  if (!analysisData || analysisData.length === 0) {
    container.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Veri bulunamadı. Lütfen önce veri yükleyin.
                <br><small>Debug: analysisData = ${analysisData ? analysisData.length + " records" : "null"}</small>
            </div>
        `
    return
  }

  // Send data to server for visualization
  fetch("/visualize", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      chart_type: chartType,
      data: analysisData,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      return response.json()
    })
    .then((data) => {
      if (data.error) {
        container.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        ${data.error}
                    </div>
                `
      } else {
        container.innerHTML = data.chart_html
      }
    })
    .catch((error) => {
      console.error("Chart loading error:", error)
      container.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Grafik yüklenirken hata oluştu: ${error.message}
                    <br><small>Chart type: ${chartType}</small>
                    <br><small>Data length: ${analysisData ? analysisData.length : "null"}</small>
                </div>
            `
    })
}

// Utility functions
function showAlert(message, type = "info") {
  const alertDiv = document.createElement("div")
  alertDiv.className = `alert alert-${type} alert-dismissible fade show`
  alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `

  const container = document.querySelector(".container")
  container.insertBefore(alertDiv, container.firstChild)

  // Auto-dismiss after 5 seconds
  setTimeout(() => {
    if (alertDiv.parentNode) {
      alertDiv.remove()
    }
  }, 5000)
}

// Theme management functions
function initializeTheme() {
  const savedTheme = localStorage.getItem("theme") || "light"
  setTheme(savedTheme)
}

function toggleTheme() {
  const currentTheme = document.documentElement.classList.contains("dark-theme") ? "dark" : "light"
  const newTheme = currentTheme === "dark" ? "light" : "dark"
  setTheme(newTheme)
}

function setTheme(theme) {
  const html = document.documentElement
  const themeIcon = document.getElementById("themeIcon")

  if (theme === "dark") {
    html.classList.remove("light-theme")
    html.classList.add("dark-theme")
    if (themeIcon) {
      themeIcon.classList.remove("fa-moon")
      themeIcon.classList.add("fa-sun")
    }
  } else {
    html.classList.remove("dark-theme")
    html.classList.add("light-theme")
    if (themeIcon) {
      themeIcon.classList.remove("fa-sun")
      themeIcon.classList.add("fa-moon")
    }
  }

  localStorage.setItem("theme", theme)
}

// Store analysis data with better error handling
function storeAnalysisData(data) {
  try {
    console.log("Storing analysis data...")
    console.log("Raw data type:", typeof data)
    console.log("Raw data sample:", data ? data.substring(0, 200) : "null")

    if (!data || data === "None" || data === "null" || data.trim() === "") {
      console.error("No valid data to store")
      analysisData = null
      return
    }

    if (typeof data === "string") {
      analysisData = JSON.parse(data)
    } else if (Array.isArray(data)) {
      analysisData = data
    } else {
      analysisData = [data]
    }

    console.log("Analysis data stored successfully:", analysisData.length, "records")
    console.log("Sample data:", analysisData.slice(0, 2))

    // Validate data structure
    if (analysisData.length > 0 && typeof analysisData[0] === "object") {
      console.log("Data columns:", Object.keys(analysisData[0]))
    }
  } catch (error) {
    console.error("Error storing analysis data:", error)
    console.error("Data received:", data)
    analysisData = null
  }
}

function loadAnalysisChart(chartType, analysisType) {
  console.log("Loading chart:", chartType, "for analysis:", analysisType)

  const container = document.getElementById(`chartContainer-${analysisType}`)
  if (!container) {
    console.error("Chart container not found:", `chartContainer-${analysisType}`)
    return
  }

  const buttons = container.parentElement.querySelectorAll(".btn-group .btn")

  // Update button states
  buttons.forEach((btn) => btn.classList.remove("active"))
  if (event && event.target) {
    event.target.classList.add("active")
  }

  // Show loading
  container.innerHTML = `
        <div class="text-center py-5">
            <i class="fas fa-spinner fa-spin fa-3x mb-3"></i>
            <p class="text-muted">Grafik oluşturuluyor...</p>
            <small class="text-info">Chart: ${chartType} | Analysis: ${analysisType}</small>
        </div>
    `

  // Check if we have analysis data
  if (!analysisData || analysisData.length === 0) {
    console.error("No analysis data available")
    container.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Veri bulunamadı. Lütfen sayfayı yenileyin.
                <br><small>Debug: analysisData = ${analysisData ? analysisData.length + " records" : "null"}</small>
            </div>
        `
    return
  }

  console.log("Sending visualization request...")

  // Send data to server for visualization with analysis context
  fetch("/visualize", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      chart_type: chartType,
      data: analysisData,
      analysis_context: {
        analysis_type: analysisType,
        title: `${analysisType} - ${chartType}`,
      },
    }),
  })
    .then((response) => {
      console.log("Response status:", response.status)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      return response.json()
    })
    .then((data) => {
      console.log("Visualization response received")
      if (data.error) {
        console.error("Server error:", data.error)
        container.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    ${data.error}
                </div>
            `
      } else {
        console.log("Chart loaded successfully")
        container.innerHTML = data.chart_html
      }
    })
    .catch((error) => {
      console.error("Chart loading error:", error)
      container.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Grafik yüklenirken hata oluştu: ${error.message}
                <br><small>Chart type: ${chartType}</small>
                <br><small>Analysis type: ${analysisType}</small>
                <br><small>Data length: ${analysisData ? analysisData.length : "null"}</small>
            </div>
        `
    })
}

// Export functions for global access
window.loadChart = loadChart
window.showAlert = showAlert
window.toggleTheme = toggleTheme
window.setTheme = setTheme
window.storeAnalysisData = storeAnalysisData
window.loadAnalysisChart = loadAnalysisChart
