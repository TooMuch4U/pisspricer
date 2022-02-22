import {BaseExceptionFilter, HttpAdapterHost} from "@nestjs/core";
import {ArgumentsHost, Catch, UnauthorizedException} from "@nestjs/common";

@Catch(UnauthorizedException)
export class BasicAuthExceptionFilter extends BaseExceptionFilter<UnauthorizedException> {
    constructor(adapterHost: HttpAdapterHost) {
        super(adapterHost.httpAdapter);
    }

    catch(exception: UnauthorizedException, host: ArgumentsHost) {
        const ctx = host.switchToHttp();
        const response = ctx.getResponse();
        const request = ctx.getRequest();
        const status = exception.getStatus()

        if (request.authInfo) {
            response
                .status(status)
                .set('WWW-Authenticate', request.authInfo)
                .send()
        } else {
            super.catch(exception, host)
        }
    }
}
