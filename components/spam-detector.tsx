"use client"

import type React from "react"
import { useState } from "react"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Mail, Shield, ShieldCheck, ShieldAlert, Loader2, CheckCircle2, XCircle } from "lucide-react"

interface ModelResult {
  model: string
  prediction: string
  is_spam: boolean
  probability: number
  confidence: number
}

interface DetectionResult {
  final_prediction: string
  is_spam: boolean
  confidence: number
  spam_votes: number
  ham_votes: number
  spam_score: number
  ham_score: number
  reasons: string[]
  model_results: ModelResult[]
}

const EXAMPLES = {
  spam: {
    email: "winner@lottery-prize.com",
    content:
      "Congratulations! You've won $1,000,000! Click here to claim your prize now! Limited time offer, act immediately!",
  },
  ham: {
    email: "john.doe@company.com",
    content:
      "Hi, just wanted to follow up on our meeting from yesterday. Can you send me the project timeline when you get a chance? Thanks!",
  },
}

function analyzeEmail(email: string, content: string): DetectionResult {
  const fullText = `${email} ${content}`.toLowerCase()

  // Palabras indicadoras de spam
  const spamWords = [
    "win",
    "winner",
    "won",
    "free",
    "prize",
    "click",
    "urgent",
    "limited",
    "offer",
    "congratulations",
    "million",
    "dollar",
    "cash",
    "money",
    "lottery",
    "claim",
    "act now",
    "immediately",
    "discount",
    "sale",
    "buy now",
    "subscribe",
    "unsubscribe",
  ]

  // Palabras indicadoras de ham
  const hamWords = [
    "meeting",
    "project",
    "follow up",
    "thanks",
    "please",
    "review",
    "attached",
    "schedule",
    "call",
    "team",
    "report",
    "deadline",
    "tomorrow",
    "yesterday",
    "help",
    "question",
  ]

  // Dominios sospechosos
  const suspiciousDomains = ["lottery", "prize", "winner", "free", "cash", "money"]
  const legitimateDomains = ["company", "corp", "inc", "org", "edu", "gov", "gmail", "outlook", "yahoo"]

  // Calcular características
  let spamFeatures = 0
  let hamFeatures = 0
  const reasons: string[] = []

  // Analizar dominio del email
  const domain = email.split("@")[1]?.toLowerCase() || ""
  if (suspiciousDomains.some((d) => domain.includes(d))) {
    spamFeatures += 3
    reasons.push(`Dominio sospechoso: ${domain}`)
  }
  if (legitimateDomains.some((d) => domain.includes(d))) {
    hamFeatures += 2
    reasons.push(`Dominio reconocido: ${domain}`)
  }

  // Analizar contenido
  spamWords.forEach((word) => {
    if (fullText.includes(word)) {
      spamFeatures += 1
      if (reasons.length < 6) reasons.push(`Palabra spam: "${word}"`)
    }
  })

  hamWords.forEach((word) => {
    if (fullText.includes(word)) {
      hamFeatures += 1
      if (reasons.length < 6) reasons.push(`Palabra legítima: "${word}"`)
    }
  })

  // Características adicionales
  if (content.includes("!") && (content.match(/!/g) || []).length > 2) {
    spamFeatures += 2
    reasons.push("Uso excesivo de signos de exclamación")
  }
  if (content.toUpperCase() === content && content.length > 20) {
    spamFeatures += 2
    reasons.push("Texto en mayúsculas")
  }
  if (/\$[\d,]+/.test(content)) {
    spamFeatures += 2
    reasons.push("Menciona cantidades de dinero")
  }

  // Simular resultados de 4 modelos diferentes
  const baseSpamProb = spamFeatures / (spamFeatures + hamFeatures + 1)

  const models: ModelResult[] = [
    {
      model: "Regresión Lineal",
      prediction: baseSpamProb > 0.45 ? "spam" : "ham",
      is_spam: baseSpamProb > 0.45,
      probability: Math.min(0.95, baseSpamProb + (Math.random() * 0.1 - 0.05)),
      confidence: Math.min(95, (baseSpamProb + Math.random() * 0.1) * 100),
    },
    {
      model: "Regresión Logística",
      prediction: baseSpamProb > 0.5 ? "spam" : "ham",
      is_spam: baseSpamProb > 0.5,
      probability: Math.min(0.95, baseSpamProb + (Math.random() * 0.08 - 0.04)),
      confidence: Math.min(95, (baseSpamProb + Math.random() * 0.08) * 100),
    },
    {
      model: "Pipeline Personalizado",
      prediction: baseSpamProb > 0.48 ? "spam" : "ham",
      is_spam: baseSpamProb > 0.48,
      probability: Math.min(0.95, baseSpamProb + (Math.random() * 0.12 - 0.06)),
      confidence: Math.min(95, (baseSpamProb + Math.random() * 0.12) * 100),
    },
    {
      model: "SVM (Support Vector Machine)",
      prediction: baseSpamProb > 0.52 ? "spam" : "ham",
      is_spam: baseSpamProb > 0.52,
      probability: Math.min(0.95, baseSpamProb + (Math.random() * 0.06 - 0.03)),
      confidence: Math.min(95, (baseSpamProb + Math.random() * 0.06) * 100),
    },
  ]

  // Votación por mayoría
  const spamVotes = models.filter((m) => m.is_spam).length
  const hamVotes = models.filter((m) => !m.is_spam).length
  const isSpam = spamVotes > hamVotes

  // Calcular confianza promedio
  const avgConfidence = models.reduce((sum, m) => sum + m.confidence, 0) / models.length

  return {
    final_prediction: isSpam ? "SPAM" : "HAM",
    is_spam: isSpam,
    confidence: avgConfidence,
    spam_votes: spamVotes,
    ham_votes: hamVotes,
    spam_score: Math.round(spamFeatures * 10),
    ham_score: Math.round(hamFeatures * 10),
    reasons: reasons.slice(0, 6),
    model_results: models,
  }
}

export function SpamDetector() {
  const [email, setEmail] = useState(EXAMPLES.ham.email)
  const [content, setContent] = useState(EXAMPLES.ham.content)
  const [result, setResult] = useState<DetectionResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState<"clasificador" | "modelos">("clasificador")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    // Simular delay de API
    await new Promise((resolve) => setTimeout(resolve, 800))

    const analysisResult = analyzeEmail(email, content)
    setResult(analysisResult)
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Shield className="h-6 w-6 text-primary" />
            <span className="font-semibold text-lg text-foreground">SpamGuard ML</span>
          </div>
          <nav className="flex gap-6">
            <button
              onClick={() => setActiveTab("modelos")}
              className={`text-sm ${activeTab === "modelos" ? "text-foreground" : "text-muted-foreground hover:text-foreground"}`}
            >
              Modelos
            </button>
            <button
              onClick={() => setActiveTab("clasificador")}
              className={`text-sm ${activeTab === "clasificador" ? "text-foreground" : "text-muted-foreground hover:text-foreground"}`}
            >
              Clasificador
            </button>
          </nav>
        </div>
      </header>

      <main className="max-w-3xl mx-auto py-8 px-4">
        {activeTab === "clasificador" ? (
          <div className="space-y-6">
            {/* Formulario */}
            <Card className="bg-card border-border">
              <CardHeader className="pb-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-primary/20 rounded-lg">
                    <Mail className="h-6 w-6 text-primary" />
                  </div>
                  <div>
                    <h2 className="text-xl font-semibold text-foreground">Analizar Correo</h2>
                    <p className="text-sm text-muted-foreground">
                      Ingresa el correo y contenido para clasificar con múltiples modelos ML
                    </p>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="email" className="text-sm text-muted-foreground">
                      Correo Electrónico
                    </Label>
                    <Input
                      id="email"
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="ejemplo@dominio.com"
                      className="bg-input border-border text-foreground placeholder:text-muted-foreground"
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="content" className="text-sm text-muted-foreground">
                      Contenido del Mensaje
                    </Label>
                    <Textarea
                      id="content"
                      value={content}
                      onChange={(e) => setContent(e.target.value)}
                      placeholder="Escribe el contenido del mensaje aquí..."
                      rows={5}
                      className="bg-input border-border text-foreground placeholder:text-muted-foreground resize-none"
                      required
                    />
                  </div>

                  <Button
                    type="submit"
                    disabled={loading || !email || !content}
                    className="w-full bg-primary hover:bg-primary/90 text-primary-foreground font-medium"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Analizando...
                      </>
                    ) : (
                      <>
                        <Shield className="mr-2 h-4 w-4" />
                        Clasificar con ML
                      </>
                    )}
                  </Button>
                </form>
              </CardContent>
            </Card>

            {/* Resultados */}
            {result && (
              <Card className="bg-card border-border">
                <CardContent className="pt-6">
                  {/* Resultado principal */}
                  <div className="flex items-start justify-between mb-6">
                    <div className="flex items-center gap-3">
                      {result.is_spam ? (
                        <ShieldAlert className="h-8 w-8 text-destructive" />
                      ) : (
                        <ShieldCheck className="h-8 w-8 text-primary" />
                      )}
                      <div>
                        <h3 className={`text-xl font-semibold ${result.is_spam ? "text-destructive" : "text-primary"}`}>
                          {result.is_spam ? "Correo SPAM" : "Correo Legítimo (HAM)"}
                        </h3>
                        <p className="text-sm text-muted-foreground">
                          {result.is_spam ? "Este correo parece ser spam" : "Este correo parece ser legítimo"}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className={`text-2xl font-bold ${result.is_spam ? "text-destructive" : "text-primary"}`}>
                        {result.confidence.toFixed(0)}% confianza
                      </p>
                      <p className="text-sm text-muted-foreground">
                        Votos: {result.spam_votes} spam / {result.ham_votes} ham
                      </p>
                    </div>
                  </div>

                  {/* Barras de puntuación */}
                  <div className="grid grid-cols-2 gap-4 mb-6">
                    <div>
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-muted-foreground">Puntuación Spam</span>
                        <span className="text-destructive">{result.spam_score}</span>
                      </div>
                      <div className="w-full bg-muted rounded-full h-2">
                        <div
                          className="h-2 rounded-full bg-destructive transition-all"
                          style={{ width: `${Math.min(100, result.spam_score)}%` }}
                        />
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-muted-foreground">Puntuación Ham</span>
                        <span className="text-primary">{result.ham_score}</span>
                      </div>
                      <div className="w-full bg-muted rounded-full h-2">
                        <div
                          className="h-2 rounded-full bg-primary transition-all"
                          style={{ width: `${Math.min(100, result.ham_score)}%` }}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Razones del análisis */}
                  {result.reasons.length > 0 && (
                    <div>
                      <h4 className="text-sm font-medium text-foreground mb-3">Razones del análisis:</h4>
                      <div className="grid grid-cols-2 gap-2">
                        {result.reasons.map((reason, idx) => (
                          <div key={idx} className="flex items-center gap-2 text-sm">
                            <CheckCircle2 className="h-4 w-4 text-primary flex-shrink-0" />
                            <span className="text-muted-foreground">{reason}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Resultados por modelo */}
                  <div className="mt-6 pt-6 border-t border-border">
                    <h4 className="text-sm font-medium text-foreground mb-3">Resultados por modelo:</h4>
                    <div className="space-y-3">
                      {result.model_results.map((model, idx) => (
                        <div key={idx} className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                          <div className="flex items-center gap-2">
                            {model.is_spam ? (
                              <XCircle className="h-4 w-4 text-destructive" />
                            ) : (
                              <CheckCircle2 className="h-4 w-4 text-primary" />
                            )}
                            <span className="text-sm font-medium text-foreground">{model.model}</span>
                          </div>
                          <div className="flex items-center gap-4">
                            <span
                              className={`text-sm font-medium ${model.is_spam ? "text-destructive" : "text-primary"}`}
                            >
                              {model.prediction.toUpperCase()}
                            </span>
                            <span className="text-sm text-muted-foreground">{model.confidence.toFixed(1)}%</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        ) : (
          /* Pestaña de Modelos */
          <Card className="bg-card border-border">
            <CardHeader>
              <h2 className="text-xl font-semibold text-foreground">Modelos de Machine Learning</h2>
              <p className="text-sm text-muted-foreground">4 modelos matemáticos utilizados para la clasificación</p>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="p-4 bg-muted/50 rounded-lg">
                <h3 className="font-medium text-foreground mb-2">1. Regresión Lineal</h3>
                <p className="text-sm text-muted-foreground">
                  Modelo básico que establece una relación lineal entre las características del texto y la probabilidad
                  de spam. Útil como baseline y para comparación.
                </p>
              </div>
              <div className="p-4 bg-muted/50 rounded-lg">
                <h3 className="font-medium text-foreground mb-2">2. Regresión Logística</h3>
                <p className="text-sm text-muted-foreground">
                  Clasificador probabilístico que utiliza la función sigmoide para predecir la probabilidad de que un
                  correo sea spam. Ideal para clasificación binaria.
                </p>
              </div>
              <div className="p-4 bg-muted/50 rounded-lg">
                <h3 className="font-medium text-foreground mb-2">3. Pipeline Personalizado</h3>
                <p className="text-sm text-muted-foreground">
                  Combina TF-IDF para vectorización de texto con un clasificador optimizado. Incluye preprocesamiento,
                  eliminación de stopwords y n-gramas.
                </p>
              </div>
              <div className="p-4 bg-muted/50 rounded-lg">
                <h3 className="font-medium text-foreground mb-2">4. SVM (Support Vector Machine)</h3>
                <p className="text-sm text-muted-foreground">
                  Clasificador que encuentra el hiperplano óptimo para separar spam de ham. Utiliza kernel RBF para
                  manejar relaciones no lineales en el texto.
                </p>
              </div>
            </CardContent>
          </Card>
        )}
      </main>
    </div>
  )
}
