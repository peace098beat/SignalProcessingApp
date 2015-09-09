
def plotFigure():
    # グラフプロット
    sp_row = 5
    sp_col = 1
    sp_i = 0
    fig = pl.figure(figsize=(5, 7), dpi=80, facecolor='white', edgecolor='black', frameon=True)

    sp_i += 1
    # wav plot
    pl.subplot(sp_row, sp_col, sp_i)
    pl.plot(trange, wavdata)
    pl.xlim(trange[0], trange[-1])
    pl.xticks([trange[0], trange[-1]])
    pl.xlabel("time [ms]")
    pl.ylabel("amplitude")
    pl.grid()

    sp_i += 1
    # powerplot
    pl.subplot(sp_row, sp_col, sp_i)
    pl.plot(fscale[1:framesize/2], 10 * np.log10(Pdft[1:framesize/2]))
    # pl.xlim(fscale[0], fscale[framesize / 2 - 1])
    # pl.xticks([trange[0],trange[-1]])
    pl.xlabel("freqency [kHz]")
    pl.ylabel("amplitude")
    pl.grid()

    sp_i += 1
    # Cepstrum
    pl.subplot(sp_row, sp_col, sp_i)
    pl.plot(quefrency, cps)

    pl.plot([cepCoef_env, cepCoef_env], [-10, 10], color="green")
    pl.plot([cepCoef_det, cepCoef_det], [-10, 10], color="c")

    pl.xlim(quefrency[0] - 5, quefrency[len(quefrency) / 2])
    # pl.xticks([trange[0],trange[-1]])
    pl.xlabel("quefrency [s]")
    pl.ylabel("amplitude")
    pl.grid()

    sp_i += 1
    # Cepstrum
    pl.subplot(sp_row, sp_col, sp_i)
    pl.plot(fscale[1:framesize/2], AdftLog[1:framesize/2])
    pl.plot(fscale[1:framesize/2], dftSpc_env[1:framesize/2], color="red")
    pl.xlim(fscale[0], fscale[framesize / 2 - 1])
    # pl.xticks([trange[0],trange[-1]])
    pl.ylim(-50, 50)
    pl.xlabel("freqency [kHz]")
    pl.ylabel("amplitude")
    pl.grid()

    sp_i += 1
    # Cepstrum
    pl.subplot(sp_row, sp_col, sp_i)
    # pl.plot(fscale, AdftLog)
    pl.plot(fscale[1:framesize/2], dftSpc_det[1:framesize/2], color="red")
    pl.xlim(fscale[0], fscale[framesize / 2 - 1])
    # pl.xticks([trange[0],trange[-1]])
    pl.ylim(-50, 50)

    pl.xlabel("freqency [kHz]")
    pl.ylabel("amplitude")
    pl.grid()

    pl.show()