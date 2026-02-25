-- ██╗  ██╗ █████╗ ██╗   ██╗███╗   ██╗████████╗███████╗██████╗     ██╗  ██╗██╗   ██╗██████╗
-- ██║  ██║██╔══██╗██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗    ██║  ██║██║   ██║██╔══██╗
-- ███████║███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██║  ██║    ███████║██║   ██║██████╔╝
-- ██╔══██║██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██║  ██║    ██╔══██║██║   ██║██╔══██╗
-- ██║  ██║██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██████╔╝    ██║  ██║╚██████╔╝██████╔╝
-- ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═════╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝

local Players    = game:GetService("Players")
local TweenService = game:GetService("TweenService")
local RunService = game:GetService("RunService")
local UIS        = game:GetService("UserInputService")
local PPS        = game:GetService("ProximityPromptService")
local CoreGui    = game:GetService("CoreGui")
local TCS        = game:GetService("TextChatService")
local plr        = Players.LocalPlayer

-- ============================================================
-- POSIÇÕES & SEQUÊNCIAS
-- ============================================================
local pos1 = Vector3.new(-352.98, -7, 74.30)
local pos2 = Vector3.new(-352.98, -6.49, 45.76)

local s1 = {
    CFrame.new(-370.810913,-7.00000334,41.2687263,0.99984771,1.22364419e-09,0.0174523517,-6.54859778e-10,1,-3.2596418e-08,-0.0174523517,3.25800258e-08,0.99984771),
    CFrame.new(-336.355286,-5.10107088,17.2327671,-0.999883354,-2.76150569e-08,0.0152716246,-2.88224964e-08,1,-7.88441525e-08,-0.0152716246,-7.9275118e-08,-0.999883354)
}
local s2 = {
    CFrame.new(-354.782867,-7.00000334,92.8209305,-0.999997616,-1.11891862e-09,-0.00218066527,-1.11958298e-09,1,3.03415071e-10,0.00218066527,3.05855785e-10,-0.999997616),
    CFrame.new(-336.942902,-5.10106993,99.3276443,0.999914348,-3.63984611e-08,0.0130875716,3.67094941e-08,1,-2.35254749e-08,-0.0130875716,2.40038975e-08,0.999914348)
}

-- ============================================================
-- LIMPA GUI ANTIGA
-- ============================================================
if CoreGui:FindFirstChild("SilentHubGui")  then CoreGui["SilentHubGui"]:Destroy()  end
if CoreGui:FindFirstChild("HauntedHubGui") then CoreGui["HauntedHubGui"]:Destroy() end
if CoreGui:FindFirstChild("SnipexHubGui")  then CoreGui["SnipexHubGui"]:Destroy()  end
if CoreGui:FindFirstChild("SnipexNotif")   then CoreGui["SnipexNotif"]:Destroy()   end

-- ============================================================
-- SCREEN GUI
-- ============================================================
local sg = Instance.new("ScreenGui")
sg.Name           = "HauntedHubGui"
sg.ResetOnSpawn   = false
sg.IgnoreGuiInset = true
sg.Parent         = CoreGui

-- ============================================================
-- ESP BOXES
-- ============================================================
local function espBox(pos, txt)
    local f = Instance.new("Folder"); f.Name = "ESP_"..txt; f.Parent = workspace
    local b = Instance.new("Part")
    b.Size = Vector3.new(5,.5,5); b.Position = pos
    b.Anchored = true; b.CanCollide = false; b.Transparency = 0.5
    b.Material = Enum.Material.Neon; b.Color = Color3.fromRGB(0,0,0); b.Parent = f
    local sb = Instance.new("SelectionBox"); sb.Adornee = b
    sb.LineThickness = 0.05; sb.Color3 = Color3.fromRGB(255,255,255); sb.Parent = b
    local bb = Instance.new("BillboardGui"); bb.Adornee = b
    bb.Size = UDim2.new(0,150,0,40); bb.StudsOffset = Vector3.new(0,2,0)
    bb.AlwaysOnTop = true; bb.Parent = b
    local tl = Instance.new("TextLabel"); tl.Size = UDim2.new(1,0,1,0)
    tl.BackgroundTransparency = 1; tl.Text = txt
    tl.TextColor3 = Color3.fromRGB(255,255,255)
    tl.TextSize = 18; tl.Font = Enum.Font.GothamBold
    tl.TextStrokeTransparency = 0.5; tl.Parent = bb
end
espBox(pos1, "Teleport Here"); espBox(pos2, "Teleport Here")
espBox(Vector3.new(-336.36,-4.59,99.51),  "Standing 1")
espBox(Vector3.new(-334.81,-4.59,18.90),  "Standing 2")
espBox(Vector3.new(-349.325867,-7.00000238,95.0031433), "Auto tp Left")
espBox(Vector3.new(-349.560211,-7.00000238,27.0543289), "Auto tp Right")

-- ============================================================
-- LÓGICA
-- ============================================================
local semiTP      = false
local speedSteal  = false
local speedConn   = nil
local SPEED       = 28
local IsStealing  = false
local StealProgress = 0
local RADIUS      = 200
local animals     = {}
local promptCache = {}

local function getRoot()   local c=plr.Character; return c and c:FindFirstChild("HumanoidRootPart") end
local function getHum()    local c=plr.Character; return c and c:FindFirstChildOfClass("Humanoid") end
local function getCarpet() local bp=plr:FindFirstChild("Backpack"); return bp and bp:FindFirstChild("Flying Carpet") end

local function equipCarpet()
    local c,h = getCarpet(), getHum()
    if c and h then h:EquipTool(c); task.wait(0.1) end
end

local function doTP(seq)
    local r = getRoot(); if not r then return end
    equipCarpet(); r.CFrame = seq[1]; task.wait(0.1); r.CFrame = seq[2]
end

-- ResetToWork: só executa quando o toggle "Ativar e Reiniciar" for ligado
local function ResetToWork()
    local flags = {
        {"GameNetPVHeaderRotationalVelocityZeroCutoffExponent","-5000"},
        {"LargeReplicatorWrite5","true"}, {"LargeReplicatorEnabled9","true"},
        {"S2PhysicsSenderRate","15000"},  {"MaxDataPacketPerSend","2147483647"},
        {"PhysicsSenderMaxBandwidthBps","20000"}, {"WorldStepMax","30"},
        {"MaxAcceptableUpdateDelay","1"}, {"LargeReplicatorSerializeWrite4","true"}
    }
    for _,d in ipairs(flags) do
        pcall(function() if setfflag then setfflag(d[1],d[2]) end end)
    end
    local char = plr.Character
    if char then
        local h = char:FindFirstChildOfClass("Humanoid")
        if h then h:ChangeState(Enum.HumanoidStateType.Dead) end
        char:ClearAllChildren()
        local f = Instance.new("Model", workspace)
        plr.Character = f; task.wait(); plr.Character = char; f:Destroy()
    end
end

-- ============================================================
-- NOTIFICAÇÃO
-- ============================================================
local notifGui = Instance.new("ScreenGui")
notifGui.Name = "SnipexNotif"; notifGui.ResetOnSpawn = false
notifGui.IgnoreGuiInset = true; notifGui.Parent = CoreGui

local nf = Instance.new("Frame")
nf.Size = UDim2.new(0,290,0,62)
nf.Position = UDim2.new(0.5,-145,-0.15,0)
nf.BackgroundColor3 = Color3.fromRGB(7,3,16)
nf.BorderSizePixel = 0; nf.Parent = notifGui
Instance.new("UICorner",nf).CornerRadius = UDim.new(0,12)
local nfS = Instance.new("UIStroke",nf); nfS.Thickness = 1.5; nfS.Color = Color3.fromRGB(80,0,255)
local nfG = Instance.new("UIGradient",nf)
nfG.Color = ColorSequence.new({
    ColorSequenceKeypoint.new(0, Color3.fromRGB(14,5,32)),
    ColorSequenceKeypoint.new(1, Color3.fromRGB(5,2,14))
})
nfG.Rotation = 120

local nIcon = Instance.new("TextLabel"); nIcon.Size = UDim2.new(0,32,0,32)
nIcon.Position = UDim2.new(0,12,0.5,-16); nIcon.BackgroundTransparency = 1
nIcon.Text = "☠"; nIcon.TextColor3 = Color3.fromRGB(180,100,255)
nIcon.TextSize = 22; nIcon.Font = Enum.Font.GothamBlack; nIcon.Parent = nf

local nTitle = Instance.new("TextLabel"); nTitle.Size = UDim2.new(1,-60,0,28)
nTitle.Position = UDim2.new(0,50,0,6); nTitle.BackgroundTransparency = 1
nTitle.Text = "HAUNTED HUB"; nTitle.TextColor3 = Color3.fromRGB(180,100,255)
nTitle.TextSize = 14; nTitle.Font = Enum.Font.GothamBlack
nTitle.TextXAlignment = Enum.TextXAlignment.Left; nTitle.Parent = nf
local nTG = Instance.new("UIGradient",nTitle)
nTG.Color = ColorSequence.new({
    ColorSequenceKeypoint.new(0,   Color3.fromRGB(220,80,255)),
    ColorSequenceKeypoint.new(0.5, Color3.fromRGB(80,210,255)),
    ColorSequenceKeypoint.new(1,   Color3.fromRGB(220,80,255))
})

local nSub = Instance.new("TextLabel"); nSub.Size = UDim2.new(1,-60,0,18)
nSub.Position = UDim2.new(0,50,0,36); nSub.BackgroundTransparency = 1
nSub.Text = "Carregado com sucesso  ·  discord.gg/vepV6dYapW"
nSub.TextColor3 = Color3.fromRGB(120,255,160); nSub.TextSize = 9
nSub.Font = Enum.Font.GothamMedium; nSub.TextXAlignment = Enum.TextXAlignment.Left; nSub.Parent = nf

TweenService:Create(nf, TweenInfo.new(0.5,Enum.EasingStyle.Back,Enum.EasingDirection.Out), {
    Position = UDim2.new(0.5,-145,0,16)
}):Play()
task.delay(3.8, function()
    TweenService:Create(nf, TweenInfo.new(0.35,Enum.EasingStyle.Quad,Enum.EasingDirection.In), {
        Position = UDim2.new(0.5,-145,-0.15,0)
    }):Play()
    task.wait(0.4); notifGui:Destroy()
end)

-- ============================================================
-- HELPERS UI
-- ============================================================
local function lbl(parent, txt, size, pos, col, fs, font, xa)
    local l = Instance.new("TextLabel"); l.Size = size; l.Position = pos
    l.BackgroundTransparency = 1; l.Text = txt
    l.TextColor3 = col or Color3.fromRGB(255,255,255)
    l.TextSize = fs or 12; l.Font = font or Enum.Font.GothamBold
    if xa then l.TextXAlignment = xa end
    l.Parent = parent; return l
end

local function mkSep(parent, yPos)
    local s = Instance.new("Frame"); s.Size = UDim2.new(0.88,0,0,1)
    s.Position = UDim2.new(0.06,0,0,yPos); s.BackgroundColor3 = Color3.fromRGB(60,0,150)
    s.BorderSizePixel = 0; s.Parent = parent
    local g = Instance.new("UIGradient",s)
    g.Color = ColorSequence.new({
        ColorSequenceKeypoint.new(0,   Color3.fromRGB(0,0,0)),
        ColorSequenceKeypoint.new(0.5, Color3.fromRGB(130,0,255)),
        ColorSequenceKeypoint.new(1,   Color3.fromRGB(0,0,0))
    })
end

local function mkToggle(parent, txt, yPos, cb, startsOn)
    local row = Instance.new("Frame"); row.Size = UDim2.new(1,-12,0,28)
    row.Position = UDim2.new(0,6,0,yPos); row.BackgroundColor3 = Color3.fromRGB(10,4,22)
    row.BorderSizePixel = 0; row.Parent = parent
    Instance.new("UICorner",row).CornerRadius = UDim.new(0,8)

    local tL = Instance.new("TextLabel"); tL.Size = UDim2.new(1,-54,1,0)
    tL.Position = UDim2.new(0,10,0,0); tL.BackgroundTransparency = 1
    tL.Text = txt; tL.TextColor3 = Color3.fromRGB(200,180,255)
    tL.TextSize = 9; tL.Font = Enum.Font.GothamMedium
    tL.TextXAlignment = Enum.TextXAlignment.Left; tL.Parent = row

    local track = Instance.new("TextButton"); track.Size = UDim2.new(0,40,0,20)
    track.Position = UDim2.new(1,-46,0.5,-10); track.Text = ""; track.BorderSizePixel = 0
    track.BackgroundColor3 = Color3.fromRGB(18,8,36); track.Parent = row
    Instance.new("UICorner",track).CornerRadius = UDim.new(1,0)
    local trkStroke = Instance.new("UIStroke",track); trkStroke.Color = Color3.fromRGB(60,0,140); trkStroke.Thickness = 1

    local dot = Instance.new("Frame"); dot.Size = UDim2.new(0,14,0,14)
    dot.Position = UDim2.new(0,3,0.5,-7); dot.BackgroundColor3 = Color3.fromRGB(130,90,255)
    dot.Parent = track
    Instance.new("UICorner",dot).CornerRadius = UDim.new(1,0)

    local on = startsOn or false

    local function setState(v)
        on = v
        TweenService:Create(dot, TweenInfo.new(0.18), {
            Position         = on and UDim2.new(1,-17,0.5,-7) or UDim2.new(0,3,0.5,-7),
            BackgroundColor3 = on and Color3.fromRGB(210,110,255) or Color3.fromRGB(130,90,255)
        }):Play()
        TweenService:Create(track, TweenInfo.new(0.18), {
            BackgroundColor3 = on and Color3.fromRGB(90,0,220) or Color3.fromRGB(18,8,36)
        }):Play()
        TweenService:Create(row, TweenInfo.new(0.18), {
            BackgroundColor3 = on and Color3.fromRGB(16,6,32) or Color3.fromRGB(10,4,22)
        }):Play()
    end

    if startsOn then setState(true) end

    track.MouseButton1Click:Connect(function()
        setState(not on)
        cb(on)
    end)

    return row, tL, track, dot, setState
end

local function mkABtn(parent, txt, yPos, accentColor)
    local b = Instance.new("TextButton"); b.Size = UDim2.new(1,-12,0,28)
    b.Position = UDim2.new(0,6,0,yPos); b.BackgroundColor3 = Color3.fromRGB(10,4,22)
    b.Text = ""; b.BorderSizePixel = 0; b.Parent = parent
    Instance.new("UICorner",b).CornerRadius = UDim.new(0,8)
    local st = Instance.new("UIStroke",b); st.Thickness = 1; st.Color = accentColor or Color3.fromRGB(100,0,255)

    local tL = Instance.new("TextLabel"); tL.Size = UDim2.new(1,-16,1,0)
    tL.Position = UDim2.new(0,12,0,0); tL.BackgroundTransparency = 1
    tL.Text = txt; tL.TextColor3 = Color3.fromRGB(220,200,255)
    tL.TextSize = 9; tL.Font = Enum.Font.GothamBold
    tL.TextXAlignment = Enum.TextXAlignment.Left; tL.Parent = b

    local acc = Instance.new("Frame"); acc.Size = UDim2.new(0,2.5,0.5,0)
    acc.Position = UDim2.new(0,0,0.25,0); acc.BackgroundColor3 = accentColor or Color3.fromRGB(100,0,255)
    acc.BorderSizePixel = 0; acc.Parent = b
    Instance.new("UICorner",acc).CornerRadius = UDim.new(1,0)

    b.MouseEnter:Connect(function()  TweenService:Create(b,TweenInfo.new(0.1),{BackgroundColor3=Color3.fromRGB(18,8,36)}):Play() end)
    b.MouseLeave:Connect(function()  TweenService:Create(b,TweenInfo.new(0.1),{BackgroundColor3=Color3.fromRGB(10,4,22)}):Play() end)
    return b, tL
end

-- ============================================================
-- FRAME PRINCIPAL (expandido)
-- ============================================================
local MW_FULL   = 200   -- largura
local MH_FULL   = 360   -- altura expandida (com tudo)
local MH_MINI   = 108   -- altura minimizada (header + 2 botões TP)
local isMinimized = false

local mf = Instance.new("Frame")
mf.Name               = "MainFrame"
mf.Size               = UDim2.new(0, MW_FULL, 0, MH_FULL)
mf.Position           = UDim2.new(1, -MW_FULL-10, 0.5, -MH_FULL/2)
mf.AnchorPoint        = Vector2.new(0, 0)
mf.BackgroundColor3   = Color3.fromRGB(7,3,16)
mf.BackgroundTransparency = 0.04
mf.BorderSizePixel    = 0
mf.Active             = true
mf.ClipsDescendants   = true   -- IMPORTANTE: recorta conteúdo ao minimizar
mf.Parent             = sg
Instance.new("UICorner",mf).CornerRadius = UDim.new(0,12)

local mfGrad = Instance.new("UIGradient",mf)
mfGrad.Color = ColorSequence.new({
    ColorSequenceKeypoint.new(0,   Color3.fromRGB(14,5,32)),
    ColorSequenceKeypoint.new(0.5, Color3.fromRGB(10,4,24)),
    ColorSequenceKeypoint.new(1,   Color3.fromRGB(5,2,12))
}); mfGrad.Rotation = 145

-- Borda arco-íris animada
local bs = Instance.new("UIStroke",mf); bs.Thickness = 1.8; bs.Transparency = 0.05
task.spawn(function()
    while sg and sg.Parent do
        for i = 0, 360, 2 do bs.Color = Color3.fromHSV(i/360,1,1); task.wait(0.012) end
    end
end)

-- Sombra
local shadow = Instance.new("Frame"); shadow.Size = UDim2.new(1,12,1,12)
shadow.Position = UDim2.new(0,-6,0,5); shadow.BackgroundColor3 = Color3.fromRGB(0,0,0)
shadow.BackgroundTransparency = 0.62; shadow.BorderSizePixel = 0; shadow.ZIndex = 0; shadow.Parent = mf
Instance.new("UICorner",shadow).CornerRadius = UDim.new(0,14)

-- ============================================================
-- HEADER (sempre visível)
-- ============================================================
local HEADER_H = 46

local hBar = Instance.new("Frame"); hBar.Size = UDim2.new(1,0,0,HEADER_H)
hBar.BackgroundColor3 = Color3.fromRGB(11,4,26); hBar.BorderSizePixel = 0; hBar.ZIndex = 2; hBar.Parent = mf
do
    Instance.new("UICorner",hBar).CornerRadius = UDim.new(0,12)
    local fix = Instance.new("Frame",hBar); fix.Size = UDim2.new(1,0,0,12)
    fix.Position = UDim2.new(0,0,1,-12); fix.BackgroundColor3 = Color3.fromRGB(11,4,26)
    fix.BorderSizePixel = 0
end
local hGrad = Instance.new("UIGradient",hBar)
hGrad.Color = ColorSequence.new({
    ColorSequenceKeypoint.new(0,   Color3.fromRGB(60,0,140)),
    ColorSequenceKeypoint.new(0.6, Color3.fromRGB(20,5,50)),
    ColorSequenceKeypoint.new(1,   Color3.fromRGB(8,3,20))
}); hGrad.Rotation = 90

-- Ícone fantasma
local iconLbl = Instance.new("TextLabel"); iconLbl.Size = UDim2.new(0,28,0,28)
iconLbl.Position = UDim2.new(0,8,0.5,-14); iconLbl.BackgroundTransparency = 1
iconLbl.Text = "☠"; iconLbl.TextColor3 = Color3.fromRGB(200,120,255)
iconLbl.TextSize = 20; iconLbl.Font = Enum.Font.GothamBlack; iconLbl.ZIndex = 3; iconLbl.Parent = hBar

-- Título
local titleLbl = lbl(hBar,"HAUNTED HUB",UDim2.new(1,-80,0,22),UDim2.new(0,40,0,4),
    Color3.fromRGB(255,255,255),14,Enum.Font.GothamBlack,Enum.TextXAlignment.Left)
titleLbl.ZIndex = 3
local tG = Instance.new("UIGradient",titleLbl)
tG.Color = ColorSequence.new({
    ColorSequenceKeypoint.new(0,   Color3.fromRGB(220,80,255)),
    ColorSequenceKeypoint.new(0.5, Color3.fromRGB(80,210,255)),
    ColorSequenceKeypoint.new(1,   Color3.fromRGB(220,80,255))
})
task.spawn(function()
    while sg and sg.Parent do tG.Offset = Vector2.new(math.sin(tick())*0.5,0); task.wait(0.03) end
end)

lbl(hBar,"F = Right  ·  G = Left",UDim2.new(1,-80,0,14),UDim2.new(0,40,0,28),
    Color3.fromRGB(100,60,180),7,Enum.Font.GothamMedium,Enum.TextXAlignment.Left).ZIndex = 3

-- ── BOTÃO MINIMIZAR / MAXIMIZAR ──────────────────────────────
local minBtn = Instance.new("TextButton")
minBtn.Size             = UDim2.new(0,30,0,30)
minBtn.Position         = UDim2.new(1,-36,0.5,-15)
minBtn.BackgroundColor3 = Color3.fromRGB(20,8,44)
minBtn.Text             = "─"
minBtn.TextColor3       = Color3.fromRGB(200,160,255)
minBtn.TextSize         = 14
minBtn.Font             = Enum.Font.GothamBlack
minBtn.BorderSizePixel  = 0
minBtn.ZIndex           = 10
minBtn.Parent           = hBar
Instance.new("UICorner",minBtn).CornerRadius = UDim.new(0,8)
local minBtnStroke = Instance.new("UIStroke",minBtn)
minBtnStroke.Thickness = 1.2; minBtnStroke.Color = Color3.fromRGB(120,0,255)

minBtn.MouseEnter:Connect(function()
    TweenService:Create(minBtn,TweenInfo.new(0.12),{BackgroundColor3=Color3.fromRGB(35,14,70)}):Play()
end)
minBtn.MouseLeave:Connect(function()
    TweenService:Create(minBtn,TweenInfo.new(0.12),{BackgroundColor3=Color3.fromRGB(20,8,44)}):Play()
end)

-- Divisória brilhante abaixo do header
local divL = Instance.new("Frame"); divL.Size = UDim2.new(1,0,0,2)
divL.Position = UDim2.new(0,0,0,HEADER_H); divL.BackgroundColor3 = Color3.fromRGB(80,0,180)
divL.BorderSizePixel = 0; divL.ZIndex = 2; divL.Parent = mf
local dG = Instance.new("UIGradient",divL)
dG.Color = ColorSequence.new({
    ColorSequenceKeypoint.new(0,   Color3.fromRGB(0,0,0)),
    ColorSequenceKeypoint.new(0.3, Color3.fromRGB(180,0,255)),
    ColorSequenceKeypoint.new(0.7, Color3.fromRGB(0,190,255)),
    ColorSequenceKeypoint.new(1,   Color3.fromRGB(0,0,0))
})

-- ============================================================
-- CONTEÚDO MINIMIZADO: apenas TP Left e TP Right
-- ============================================================
local MINI_Y = HEADER_H + 4   -- logo abaixo do header

local miniContainer = Instance.new("Frame")
miniContainer.Name = "MiniContainer"
miniContainer.Size = UDim2.new(1,0,0,MH_MINI - HEADER_H - 4)
miniContainer.Position = UDim2.new(0,0,0,MINI_Y)
miniContainer.BackgroundTransparency = 1
miniContainer.Visible = false   -- só aparece quando minimizado
miniContainer.Parent = mf

local miniBtnL, miniBtnLLbl = mkABtn(miniContainer,"◀  Auto TP Left   [G]",  2,  Color3.fromRGB(120,0,255))
local miniBtnR, miniBtnRLbl = mkABtn(miniContainer,"▶  Auto TP Right  [F]",  34, Color3.fromRGB(0,190,255))

-- ============================================================
-- CONTEÚDO EXPANDIDO
-- ============================================================
local FULL_Y = HEADER_H + 6

local fullContainer = Instance.new("Frame")
fullContainer.Name = "FullContainer"
fullContainer.Size = UDim2.new(1,0,0,MH_FULL - HEADER_H - 6)
fullContainer.Position = UDim2.new(0,0,0,FULL_Y)
fullContainer.BackgroundTransparency = 1
fullContainer.Visible = true
fullContainer.Parent = mf

-- Seção: Configurações
lbl(fullContainer,"CONFIGURAÇÕES",UDim2.new(1,-12,0,11),UDim2.new(0,10,0,0),
    Color3.fromRGB(100,65,190),7,Enum.Font.GothamBlack,Enum.TextXAlignment.Left)

mkToggle(fullContainer,"Half TP",          14,   function(s) semiTP