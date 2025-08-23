#include <bits/stdc++.h>
using namespace std;

int main(int argc, char** argv) {
    int batch = 100;
    if (argc > 1) batch = stoi(argv[1]);
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> dis(-1.0, 1.0);
    int c = 0;
    vector<pair<double,double>> pts;
    pts.reserve(batch);
    for (int i = 0; i < batch; ++i) {
        double x = dis(gen);
        double y = dis(gen);
        pts.emplace_back(x,y);
        if (x*x + y*y <= 1.0) ++c;
    }
    // print JSON
    cout << "{";
    cout << "\"points\": [";
    for (size_t i=0;i<pts.size();++i){
        cout << "[" << pts[i].first << "," << pts[i].second << "]";
        if (i+1<pts.size()) cout << ",";
    }
    cout << "],";
    cout << "\"circle\":" << c << ",";
    cout << "\"total\":" << batch;
    cout << "}" << flush;
    return 0;
}
