// Modello esplorativo nel dominio del tempo. Compilare con c++ -std=c++17 -O2.
#include <array>
#include <cmath>
#include <complex>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <vector>

struct Audio {
    double fondamentale;
    double distorsione_2_3;
};

Audio simula(double vrms, double is, double nvt, double cj, int passi) {
    constexpr double pi = 3.14159265358979323846;
    constexpr double fin = 10.695e6, fa = 1000, m = .80;
    constexpr double rs = 1000, cin = 10e-9, rin = 6800, rload = 47000, co = 120e-12;
    const double dt = 1/(fin*passi);
    const int campioni = static_cast<int>(std::lround(fin/fa))*passi;
    const double rs_eq = rs+dt/cin;
    const double ra = 1/(1/rin+1/rs_eq), ro = 1/(1/rload+co/dt);
    std::vector<double> portante(passi);
    for (int i=0; i<passi; ++i) portante[i] = std::cos(2*pi*i/passi);
    double vc = 0, vo = 0, vd = 0;
    std::array<std::complex<double>,3> armoniche{};
    for (int i=0; i<2*campioni; ++i) {
        const double fase = 2*pi*(i%campioni)/campioni;
        const double vs = std::sqrt(2.)*vrms*(1+m*std::cos(fase))*portante[i%passi];
        const double a0 = ra*(vs-vc)/rs_eq, o0 = ro*co/dt*vo;
        const double prev = vd;
        // Equivalenti di Thevenin dei nodi dopo discretizzazione implicita.
        for (int iter=0; iter<20; ++iter) {
            const double esp = std::exp(vd/nvt);
            const double id = is*std::expm1(vd/nvt)+cj/dt*(vd-prev);
            const double errore = vd+(ra+ro)*id-(a0-o0);
            const double passo = errore/(1+(ra+ro)*(is*esp/nvt+cj/dt));
            vd -= passo;
            if (std::abs(passo)<1e-14) break;
            if (iter==19) throw std::runtime_error("diodo: convergenza");
        }
        const double corrente = (a0-o0-vd)/(ra+ro);
        const double va = a0-ra*corrente;
        vo = o0+ro*corrente;
        vc += dt/cin*(vs-va-vc)/rs_eq;
        if (i>=campioni) {
            const auto base = std::polar(1.,-fase);
            auto fattore = base;
            for (auto &h : armoniche) { h += vo*fattore; fattore *= base; }
        }
    }
    return {2*std::abs(armoniche[0])/campioni,
            std::hypot(std::abs(armoniche[1]),std::abs(armoniche[2]))/std::abs(armoniche[0])};
}

int main() {
    // Is, nVT e Cj sono scenari ipotetici, non un modello OEM della BAT85S.
    std::cout << "Vrms_thevenin Is_A passi audio_picco_uV H2H3_percento coerente_ideale_uV\n";
    for (double vrms : {30e-6,.01,.1}) {
        for (double is : {1e-8,1e-7}) {
            for (int passi : {96,192}) {
                auto a = simula(vrms,is,.030,8e-12,passi);
                std::cout << std::setprecision(5) << vrms << ' ' << is << ' ' << passi
                          << ' ' << a.fondamentale*1e6 << ' ' << 100*a.distorsione_2_3
                          << ' ' << .8*std::sqrt(2.)*vrms*1e6 << '\n';
            }
        }
    }
}
