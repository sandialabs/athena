typedef long cnn_int;

typdef struct TimeloopCNN{
    cnn_int w;
    cnn_int h;
    cnn_int c;
    cnn_int n;
    cnn_int k;
    cnn_int s;
    cnn_int r;
    cnn_int wpad;
    cnn_int hpad;
    cnn_int wstride;
    cnn_int wdilation;
    cnn_int hdilation;
    cnn_int q;
    cnn_int r
} timeloop_cnn;

typdef struct TimeloopGEMM{

}

void init_timeloop_cnn(cnn_int w, cnn_int h, cnn_int c, cnn_int n, cnn_int k,
                        cnn_int s, cnn_int r, cnn_int wpad, cnn_int hpad,
                        cnn_int wstride, cnn_int wdilation, timeloop_cnn *t){
                        q = cnn_int(double((w - s + 2 * wpad) / wstride)+ 1)
                        p = cnn_int(double((h - r + 2 * wpad) / wstride)+ 1)
                        t->w=w;
                        t->h=h;
                        t->c=c;
                        t->n=n;
                        t->k=k;
                        t->s=s;
                        t->r=r;
                        t->wpad=wpad;
                        t->hpad=hpad;
                        t->wstride=wstride;
                        t->wdilation=wdilation;
                        t->hdilation=hdilation;
                        t->q=q;
                        t->r=r;
                        }

timeloop_cnn *t new_timeloop_cnn(cnn_int w, cnn_int h, cnn_int c, cnn_int n, cnn_int k,
                        cnn_int s, cnn_int r, cnn_int wpad, cnn_int hpad,
                        cnn_int wstride, cnn_int wdilation, timeloop_cnn *t){

                            timeloop_cnn *t = calloc(sizeof(timeloop_cnn),1)
                            init_timeloop_cnn( w, h, c, n, k, s, r, w,pad h,pad w,stride w,dilation h,dilation q, r, t)
                            return t;
                        }