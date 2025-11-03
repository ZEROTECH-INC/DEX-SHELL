// motion_tracker.cpp
// Build: see CMakeLists.txt below

#include <opencv2/opencv.hpp>
#include <vector>
#include <string>
#include <iostream>

using namespace cv;
using namespace std;

// Very simple hand centroid + contour-based pseudo-landmark extractor for prototyping.

struct Landmarks {
    int seq_id;
    vector<Point2f> points; // normalized [0..1]
};

extern "C" {

// Initialize device (index)
int mt_init(int cam_index) {
    VideoCapture cap(cam_index);
    if (!cap.isOpened()) {
        return -1;
    }
    cap.release();
    return 0;
}

// Capture a single frame and return serialized landmark string (CSV of x1,y1,x2,y2,...)
// Memory ownership: returns a malloc'd char* that must be freed by caller using free()

char* mt_capture_landmarks(int cam_index) {
    VideoCapture cap(cam_index);
    if (!cap.isOpened()) {
        const char* err = "ERR:CAM_OPEN";
        char* out = (char*)malloc(strlen(err)+1);
        strcpy(out, err);
        return out;
    }

    Mat frame;
    cap >> frame;
    if (frame.empty()) {
        const char* err = "ERR:FRAME_EMPTY";
        char* out = (char*)malloc(strlen(err)+1);
        strcpy(out, err);
        cap.release();
        return out;
    }

    // convert to HSV and threshold for skin-like colors (basic heuristic)
    Mat hsv;
    cvtColor(frame, hsv, COLOR_BGR2HSV);

    Scalar lower(0, 30, 60); // tweak these
    Scalar upper(20, 150, 255);
    Mat mask;
    inRange(hsv, lower, upper, mask);

    // morphological clean
    Mat kernel = getStructuringElement(MORPH_ELLIPSE, Size(5,5));
    morphologyEx(mask, mask, MORPH_OPEN, kernel);
    morphologyEx(mask, mask, MORPH_CLOSE, kernel);

    vector<vector<Point>> contours;
    findContours(mask, contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);

    if (contours.empty()) {
        const char* none = "NONE";
        char* out = (char*)malloc(strlen(none)+1);
        strcpy(out, none);
        cap.release();
        return out;
    }

    // find largest contour
    size_t best = 0;
    double bestArea = 0;
    for (size_t i = 0; i < contours.size(); ++i) {
        double a = contourArea(contours[i]);
        if (a > bestArea) { bestArea = a; best = i; }
    }

    vector<Point> hull;
    convexHull(contours[best], hull);

    // sample up to 21 points along hull to mimic landmarks
    int desired = 21;
    vector<Point2f> landmarks;
    double per = (double)hull.size() / (double)desired;
    for (int i = 0; i < desired; ++i) {
        int idx = (int)round(i * per) % hull.size();
        Point2f p = hull[idx];
        landmarks.push_back(p);
    }

    // normalize
    int w = frame.cols, h = frame.rows;
    std::ostringstream oss;
    for (size_t i = 0; i < landmarks.size(); ++i) {
        float nx = landmarks[i].x / (float)w;
        float ny = landmarks[i].y / (float)h;
        oss << nx << "," << ny;
        if (i + 1 < landmarks.size()) oss << ",";
    }

    string outstr = oss.str();
    char* out = (char*)malloc(outstr.size() + 1);
    strcpy(out, outstr.c_str());

    cap.release();
    return out;
}

} // extern "C"